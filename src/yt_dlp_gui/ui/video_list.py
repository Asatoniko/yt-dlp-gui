from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QHeaderView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from yt_dlp_gui.ui.actions import ActionButtons
from yt_dlp_gui.mvc.url_store import URLStore
from yt_dlp_gui.utils.models import VideoData

class VideoList(QWidget):
  layout: QVBoxLayout
  download_clicked = Signal(VideoData)

  def __init__(self, store: URLStore) -> None:
    super().__init__()
    self.store = store
    self.layout = QVBoxLayout()

    self._tree = QTreeWidget()
    self._tree.setColumnCount(7)
    self._tree.setHeaderLabels(["URL", "Extension", "Resolution", "Subtitles", "Thumbnail", "Metadata", "Actions"])

    self._header_section()

    self.layout.addWidget(self._tree)
    self.setLayout(self.layout)

  def _header_section(self) -> None:
    self._header = self._tree.header()
    self._header.setStretchLastSection(False)
    self._header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    for i in range(1, 6):
      self._header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)


  def sync_with_store(self, videos: list[VideoData]) -> None:
    self._tree.clear()
    for video in videos:
      self.add_item(video)

  def _handle_item_removal(self, item: QTreeWidgetItem, url: str) -> None:
    index = self._tree.indexOfTopLevelItem(item)
    self._tree.takeTopLevelItem(index)
    self.store.remove_video(url)

  def _handle_item_download(self, item: QTreeWidgetItem, url: str) -> None:
    video = self.store.get_by_url(url)
    if video:
      self.download_clicked.emit(video)
    self._handle_item_removal(item, url)

  def add_item(self, video:VideoData) -> None:
    item = QTreeWidgetItem(self._tree)
    self._configure_item(item, video)

    actions = ActionButtons()

    actions.remove_requested.connect(
      lambda: self._handle_item_removal(item, video.url),
    )
    actions.download_requested.connect(
      lambda: self._handle_item_download(item, video.url),
    )
    self._tree.setItemWidget(item, 6, actions)

  def _configure_item(self, item: QTreeWidgetItem, video: VideoData) -> None:
    item.setText(0, video.url)
    item.setText(1, video.extension)
    item.setText(2, video.resolution)
    item.setText(4, "+" if video.thumbnail else "–") #noqa: RUF001
    item.setText(3, "+" if video.subtitles else "–") #noqa: RUF001
    item.setText(5, "+" if video.metadata else "–") #noqa: RUF001
    for i in range(1,6):
      item.setTextAlignment(i, Qt.AlignmentFlag.AlignCenter)
    font = QFont()
    font.setPointSize(15)
    font.setBold(True)
    for i in range(3, 6):
      item.setFont(i,font)
    font.setPointSize(10)
    for i in range(1, 3):
      item.setFont(i, font)