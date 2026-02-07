from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon

class ActionButtons(QWidget):
  download_requested = Signal()
  remove_requested = Signal()

  def __init__(self) -> None:
    super().__init__()
    self.setMinimumHeight(40)
    self._layout = QHBoxLayout(self)
    self._setup()

  def _setup(self) -> None:
    self._create_elements()
    self._add_to_layout()
    self._setup_elements()

  def _create_elements(self) -> None:
    self._download_btn = QPushButton()
    self._remove_btn = QPushButton()

  def _setup_elements(self) -> None:
    self._download_btn.setIcon(QIcon(":/icons/download_btn.svg"))
    self._remove_btn.setIcon(QIcon(":/icons/remove_btn.svg"))
    self._remove_btn.clicked.connect(self.remove_requested.emit)
    self._download_btn.clicked.connect(self.download_requested.emit)

  def _add_to_layout(self) -> None:
    self._layout.addWidget(self._download_btn)
    self._layout.addWidget(self._remove_btn)
