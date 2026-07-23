import logging
from pathlib import Path
from datetime import datetime
from core.config import cfg_mgr
from typing import Optional

def setup_logger(debug_mode: bool = False):
    logger = logging.getLogger("ArenaCLI")
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    
    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # File handler in ~/.arena_cli
    log_file = cfg_mgr.config_dir / "arena_cli.log"
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger

logger = setup_logger()

async def dump_diagnostic_info(page, prefix: str = "error"):
    """Dumps screenshot and HTML to aid in debugging Playwright failures."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    diag_dir = cfg_mgr.config_dir / "diagnostics"
    diag_dir.mkdir(exist_ok=True)
    
    screenshot_path = diag_dir / f"{prefix}_{timestamp}.png"
    html_path = diag_dir / f"{prefix}_{timestamp}.html"
    
    try:
        await page.screenshot(path=str(screenshot_path))
        html_content = await page.content()
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.error(f"Diagnostics saved to {screenshot_path} and {html_path}")
        return screenshot_path, html_path
    except Exception as e:
        logger.error(f"Failed to save diagnostics: {e}")
        return None, None
