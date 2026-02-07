from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import QStandardPaths
from yt_dlp_gui.utils.utils import render_svg

class DirectoryPicker(QWidget):
  _layout: QHBoxLayout

  def __init__(self) -> None:
    super().__init__()
    self._layout = QHBoxLayout(self)
    self._icon_size = 50
    self._icon_path = ":/icons/folder-search.svg"
    self.path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)

    self.setup_ui()

  def setup_ui(self) -> None:
    self._create_elements()
    self._setup_layout()
    self._add_logic()

  def _create_elements(self) -> None:
    self._icon = QLabel()
    self._text = QLabel("Save to:")
    self.path_display = QLineEdit()
    self.path_display.setText(str(self.path))
    self._browse_btn = QPushButton("Browse..")

  def _add_logic(self) -> None:
    self._icon.setPixmap(render_svg(self._icon, self._icon_path, self._icon_size))
    self.path_display.setReadOnly(True)
    self._browse_btn.clicked.connect(self._choose_dir)

  def _setup_layout(self) -> None:
    self._layout.addWidget(self._icon)
    self._layout.addWidget(self._text)
    self._layout.addWidget(self.path_display)
    self._layout.addWidget(self._browse_btn)

  def _choose_dir(self) -> None:
    self.path = QFileDialog.getExistingDirectory(
      self, "Select Download Directory", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation),
    )
    if self.path:
      self.path_display.setText(self.path)

  def get_path(self) -> str:
    return self.path_display.text()