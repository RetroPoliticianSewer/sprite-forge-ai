"""Main window: prompt panel, preview grid, export bar."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QComboBox, QSpinBox, QPushButton, QLabel, QGridLayout,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QThreadPool

from spriteforge.config.schema import Config
from spriteforge.core.engine import SpriteEngine
from spriteforge.core.prompt import SpriteRequest
from spriteforge.handlers.generate_handler import GenerateTask


class MainWindow(QMainWindow):
    def __init__(self, engine: SpriteEngine, cfg: Config) -> None:
        super().__init__()
        self.engine = engine
        self.cfg = cfg
        self.pool = QThreadPool.globalInstance()
        self.setWindowTitle(f"sprite-forge-ai {cfg.app.version}")
        self.resize(960, 640)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)

        bar = QHBoxLayout()
        self.subject = QLineEdit()
        self.subject.setPlaceholderText("knight with a lantern, side view")
        self.kind = QComboBox(); self.kind.addItems(["character", "enemy", "item", "tile", "effect", "ui"])
        self.palette = QComboBox(); self.palette.addItems(["nes", "snes", "gb", "modern"])
        self.seed = QSpinBox(); self.seed.setRange(0, 2**31 - 1); self.seed.setValue(self.cfg.generation.seed)
        self.go = QPushButton("Generate")
        self.go.clicked.connect(self._on_generate)

        for w in (self.subject, self.kind, self.palette, self.seed, self.go):
            bar.addWidget(w)
        layout.addLayout(bar)

        self.grid = QGridLayout()
        layout.addLayout(self.grid)
        self.status = QLabel("ready")
        layout.addWidget(self.status)
        self.setCentralWidget(root)

    def _on_generate(self) -> None:
        req = SpriteRequest(
            subject=self.subject.text().strip() or "pixel knight",
            kind=self.kind.currentText(),
            palette=self.palette.currentText(),
            seed=self.seed.value(),
            count=4,
        )
        self.status.setText("generating...")
        task = GenerateTask(self.engine, req)
        task.signals.finished.connect(self._on_finished)
        task.signals.failed.connect(lambda msg: self.status.setText(f"error: {msg}"))
        self.pool.start(task)

    def _on_finished(self, result) -> None:
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for i, frame in enumerate(result.frames):
            lbl = QLabel()
            pix = QPixmap.fromImage(_pil_to_qimage(frame)).scaled(
                128, 128, Qt.KeepAspectRatio, Qt.FastTransformation
            )
            lbl.setPixmap(pix)
            self.grid.addWidget(lbl, i // 4, i % 4)
        self.status.setText(f"done — seed={result.seed} backend={result.backend}")


def _pil_to_qimage(img):
    from PySide6.QtGui import QImage
    rgba = img.convert("RGBA")
    data = rgba.tobytes("raw", "RGBA")
    return QImage(data, rgba.width, rgba.height, QImage.Format_RGBA8888).copy()