"""Wires a Generate button click to the engine and streams results to the UI."""
from __future__ import annotations

from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from spriteforge.core.engine import SpriteEngine, SpriteResult
from spriteforge.core.prompt import SpriteRequest


class GenerateSignals(QObject):
    finished = Signal(object)   # SpriteResult
    failed = Signal(str)


class GenerateTask(QRunnable):
    """Runs one generation job on the Qt thread pool. Never touches the UI directly."""

    def __init__(self, engine: SpriteEngine, req: SpriteRequest) -> None:
        super().__init__()
        self.engine = engine
        self.req = req
        self.signals = GenerateSignals()

    @Slot()
    def run(self) -> None:
        try:
            result: SpriteResult = self.engine.generate_sprite(self.req)
        except Exception as exc:  # noqa: BLE001 — surface any backend failure to UI
            self.signals.failed.emit(str(exc))
            return
        self.signals.finished.emit(result)