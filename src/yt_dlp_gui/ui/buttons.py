from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal
from yt_dlp_gui.ui.mode_button import ModeButton

class Buttons(QWidget):
  change_theme = Signal()
  download_all = Signal()
  remove_all = Signal()

  def __init__(self) -> None:
    super().__init__()
    self._create_button_section()

  def _create_button_section(self) -> None:
    self.button_layout = QHBoxLayout(self)
    self.mode_button = ModeButton(width=100)
    self.download_all_btn = QPushButton("Download All")
    self.remove_all_btn = QPushButton("Remove All")
    self.mode_button.clicked.connect(self.change_theme.emit)
    self.download_all_btn.clicked.connect(self.download_all.emit)
    self.remove_all_btn.clicked.connect(self.remove_all.emit)

    self.button_layout.addWidget(self.download_all_btn)
    self.button_layout.addWidget(self.remove_all_btn)
    self.button_layout.addWidget(self.mode_button)
