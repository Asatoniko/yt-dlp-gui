from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

class UrlInput(QWidget):
  add_url = Signal()
  search_info = Signal()

  def __init__(self) -> None:
    super().__init__()
    self._create_elements()
    self._add_selectors()
    self._add_to_layout()
    self._setup_connections()

  def _create_elements(self) -> None:
    self.input_layout = QVBoxLayout(self)
    self.video_url = QLabel("Video URL")
    self.url_input_layout = QHBoxLayout()
    self.url_input = QLineEdit(placeholderText="Paste URL here...")
    self.paste_button = QPushButton()
    self.add_button = QPushButton()
    self.search_button = QPushButton()

  def _add_selectors(self) -> None:
    self.url_input.setObjectName("inputLineEdit")
    self.video_url.setObjectName("inputLabel")
    self.paste_button.setObjectName("inputButton")
    self.add_button.setObjectName("inputButton")
    self.search_button.setObjectName("inputButton")

  def _setup_connections(self) -> None:
    self.paste_button.setIcon(QIcon(":/icons/paste.svg"))
    self.paste_button.clicked.connect(self._paste)
    self.add_button.setIcon(QIcon(":/icons/add.svg"))
    self.add_button.clicked.connect(self.add_url.emit)
    self.search_button.setIcon(QIcon(":/icons/search.svg"))
    self.search_button.clicked.connect(self.search_info.emit)

  def _add_to_layout(self) -> None:
    self.url_input_layout.addWidget(self.url_input)
    self.url_input_layout.addWidget(self.search_button)
    self.url_input_layout.addWidget(self.paste_button)
    self.url_input_layout.addWidget(self.add_button)
    self.input_layout.addWidget(self.video_url)
    self.input_layout.addLayout(self.url_input_layout)

  def _paste(self) -> None:
    clipboard = QApplication.clipboard().text()
    if clipboard:
      self.url_input.clear()
      self.url_input.setText(clipboard)