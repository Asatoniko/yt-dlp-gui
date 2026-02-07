from PySide6.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QHBoxLayout, QLabel
from yt_dlp_gui.utils.models import DownloadDetails

class ProgressBar(QWidget):
  def __init__(self) -> None:
    super().__init__()
    self._layout = QVBoxLayout(self)
    self._create_elements()
    self._setup_elements()

    self._layout.addLayout(self._eta_title_layout)
    self._layout.addWidget(self._progress_bar)
    self._layout.addLayout(self._details_layout)

  def _create_elements(self) -> None:
    self._progress_bar = QProgressBar()
    self._eta_title_layout = QHBoxLayout()
    self._eta = QLabel("00:00")
    self._title = QLabel("None")
    self._details_layout = QHBoxLayout()
    self._speed = QLabel("N/A")
    self._size = QLabel("N/A")
    self._status = QLabel("Unknown")

  def _setup_elements(self) -> None:
    self._progress_bar.setMinimum(0)
    self._progress_bar.setMaximum(100)
    self._progress_bar.setTextVisible(True)

    self._eta_title_layout.addWidget(self._eta)
    self._eta_title_layout.addWidget(self._title)
    self._details_layout.addWidget(self._speed)
    self._details_layout.addWidget(self._size)
    self._details_layout.addWidget(self._status)

  def update_bar(self, percent: int) -> None:
    self._progress_bar.setValue(percent)

  def update_details(self, details: DownloadDetails) -> None:
    self._eta.setText(details.time)
    if details.title != "":
      self._title.setText(details.title)
    self._speed.setText(details.speed)
    self._size.setText(details.size)
    self._status.setText(details.status)


