import time
import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from core.config import cfg_mgr, Sel, MODES
from utils.errors import BrowserInitError, GenerationTimeoutError
from utils.logging import logger, dump_diagnostic_info
from ui.display import get_spinner, print_info, print_error

class ArenaBrowser:
    def __init__(self, headless: bool = True, debug: bool = False):
        self.headless = headless
        self.debug = debug
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self._playwright = None

    async def start(self):
        try:
            self._playwright = await async_playwright().start()
            self.browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=["--no-sandbox", "--disable-dev-shm-usage"] + (["--start-maximized"] if not self.headless else [])
            )
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 900} if self.headless else None,
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
            
            # Load cookies
            cookies = cfg_mgr.load_cookies()
            if cookies:
                await self.context.add_cookies(cookies)
                
            self.page = await self.context.new_page()
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise BrowserInitError(f"Playwright initialization failed: {e}")

    async def stop(self):
        # Save cookies before stopping
        if self.context and cfg_mgr.config.cookie_save:
            cookies = await self.context.cookies()
            cfg_mgr.save_cookies(cookies)
            
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def login_visible(self):
        """Perform a visible login and save cookies."""
        await self.start()
        await self.page.goto("https://arena.ai/", wait_until="domcontentloaded")
        print_info("\n[cyan]Navigateur ouvert → connecte-toi sur Arena.ai[/cyan]")
        input("\nUne fois connecté au chat, appuie sur Entrée ici pour sauvegarder la session...")
        await self.stop()

    async def check_logged_in(self) -> bool:
        """Robust check for logged-in status using positive signals."""
        try:
            await self.page.goto("https://arena.ai/", wait_until="networkidle", timeout=25000)
            await self.page.wait_for_timeout(1500)

            # Strong negative signal: Login buttons
            login_btn = self.page.locator(f"{Sel.LOGIN_BTN[0]}").or_(self.page.locator(f"{Sel.LOGIN_BTN[1]}"))
            if await login_btn.count() > 0:
                if self.debug:
                    logger.debug("Login button found, not logged in.")
                    await dump_diagnostic_info(self.page, "not_logged_in")
                return False

            # Positive signal: chat input
            for sel in Sel.INPUT:
                if await self.page.locator(sel).count() > 0:
                    return True

            # Positive signal fallback: user menu
            for sel in Sel.USER_MENU:
                if await self.page.locator(sel).count() > 0:
                    return True

            if self.debug:
                logger.debug("No positive signals found, assuming not logged in.")
                await dump_diagnostic_info(self.page, "no_positive_signals")
                
            return False
        except Exception as e:
            logger.error(f"check_logged_in error: {e}")
            if self.debug:
                await dump_diagnostic_info(self.page, "check_logged_in_exception")
            return False

    async def navigate_to_mode(self, mode_key: str):
        if mode_key not in MODES:
            return
        _, url = MODES[mode_key]
        try:
            await self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await self.page.wait_for_timeout(2000)
        except Exception as e:
            logger.error(f"Failed to navigate to mode {mode_key}: {e}")

    async def get_available_models(self) -> list[str]:
        models = []
        try:
            triggers = [
                'button[aria-haspopup="listbox"]',
                'button[aria-haspopup="menu"]',
                '[data-testid="model-selector"]',
                'button:has-text("Model")',
                'button:has-text("GPT")',
                'button:has-text("Claude")',
                'button:has-text("Gemini")',
            ]
            for sel in triggers:
                btn = self.page.locator(sel).first
                if await btn.count() > 0:
                    await btn.click()
                    await self.page.wait_for_timeout(1000)
                    options = self.page.locator('[role="option"], [role="menuitem"]')
                    count = await options.count()
                    for i in range(count):
                        text = await options.nth(i).inner_text()
                        if text.strip():
                            models.append(text.strip())
                    await self.page.keyboard.press("Escape")
                    break
        except Exception as e:
            logger.debug(f"Failed to get available models: {e}")
        return models

    async def send_message(self, message: str) -> str:
        # 1. Find input area
        textarea = None
        for sel in Sel.INPUT:
            el = self.page.locator(sel).first
            if await el.count() > 0:
                textarea = el
                break

        if textarea is None:
            if self.debug:
                await dump_diagnostic_info(self.page, "textarea_not_found")
            return "[Erreur] Zone de saisie introuvable. Essaie /clear pour recharger la page."

        # 2. Type message safely (contenteditable compatible)
        await textarea.click()
        await textarea.press("Control+a")
        await textarea.press("Delete")
        await self.page.wait_for_timeout(100)
        await textarea.type(message, delay=20)
        await self.page.wait_for_timeout(200)

        # 3. Click Send
        sent = False
        for sel in Sel.SEND:
            btn = self.page.locator(sel).first
            if await btn.count() > 0 and await btn.is_enabled():
                await btn.click()
                sent = True
                break
        if not sent:
            await textarea.press("Enter")

        # 4. Wait for generation completion using Stop/Send button heuristics
        return await self._wait_for_generation_and_extract()

    async def _exists_any(self, selectors: list[str]) -> bool:
        for s in selectors:
            if await self.page.locator(s).count() > 0:
                return True
        return False

    async def _wait_for_generation_and_extract(self) -> str:
        await self.page.wait_for_timeout(1500)
        
        start = time.time()
        generation_started = False
        timeout = 120

        with get_spinner("Arena réfléchit..."):
            while time.time() - start < timeout:
                await self.page.wait_for_timeout(500)

                stop_exists = await self._exists_any(Sel.STOP)
                if stop_exists:
                    generation_started = True

                # If it started generating and stop button is gone, we are done
                if generation_started and not stop_exists:
                    break
                    
                # Alternatively, if Send is re-enabled, it's done
                if generation_started:
                    send_enabled = False
                    for s in Sel.SEND:
                        btn = self.page.locator(s).first
                        if await btn.count() > 0 and await btn.is_enabled():
                            send_enabled = True
                            break
                    if send_enabled:
                        break

            # If loop finished, wait a bit for DOM to settle
            await self.page.wait_for_timeout(500)

            # Extract response
            for sel in Sel.ASSISTANT:
                els = self.page.locator(sel)
                if await els.count() > 0:
                    try:
                        text = await els.last.inner_text()
                        if text.strip():
                            return text.strip()
                    except Exception:
                        continue
                        
        if self.debug:
            await dump_diagnostic_info(self.page, "generation_extraction_failed")
            
        return "[Erreur] Impossible de récupérer la réponse, ou timeout."
