"""Desktop entry point. Boots the Qt app, wires the main window to the engine."""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from spriteforge.config.loader import load_config
from spriteforge.core.engine import SpriteEngine
from spriteforge.ui.main_window import MainWindow
from spriteforge.utils.logging import get_logger

log = get_logger(__name__)


def main() -> int:
    cfg = load_config(Path("config/default.toml"))
    log.info("sprite-forge-ai %s booting (backend=%s)", cfg.app.version, cfg.generation.backend)

    app = QApplication(sys.argv)
    engine = SpriteEngine(cfg)
    window = MainWindow(engine, cfg)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())