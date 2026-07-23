# Changelog

## [2.0.1] - 2026-07-24

### Fixed
- Fixed a fatal crash due to `a-enter` keybinding with `prompt_toolkit`. It is now `Esc` then `Enter`.
- Installer scripts now launch the CLI automatically after completion.

### Changed
- Playwright now uses `storage_state` instead of `cookies.json` to properly persist `localStorage` and `sessionStorage`.
- The CLI now performs an automatic visible login prompt on the first run if the session is invalid, removing the need for manual `--login` calls.

## [2.0.0] - 2026-07-23

### Added
- Modular architecture with `core`, `ui`, and `utils` packages.
- Rich terminal UI with Markdown rendering, panels, and spinners.
- Interactive mode menu using `questionary`.
- Autocompletion for slash commands (`/mode`, `/models`, etc.) using `prompt_toolkit`.
- Multiline input support (use `Alt+Enter` for newline).
- Session history saving in both JSON and Markdown formats (`/save`, `/history`).
- Diagnostic mode (`--debug`) with a `/doctor` command to output screenshots and HTML.
- Robust installers for Windows (`.bat`) and macOS/Linux (`.sh`) using virtual environments.
- Support for colorama on Windows terminals.

### Changed
- Improved Playwright selectors for checking logged-in status using positive UI signals rather than heuristic fallbacks.
- Improved chat box selection and input injection for better reliability with `contenteditable` elements.
- Generation completion now waits for UI state changes ("Stop" button hiding / "Send" button enabling) rather than text stability over time.
- Migrated CLI argument parsing to `typer`.
