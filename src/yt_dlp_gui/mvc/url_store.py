from PySide6.QtCore import QObject, Signal
from yt_dlp_gui.utils.models import VideoData
from yt_dlp_gui.utils.utils import validate_url

class URLStore(QObject):
  list_changed = Signal()

  def __init__(self) -> None:
    super().__init__()
    self._videos: list[VideoData] = []

  def add_video(self, video: VideoData) -> bool:
    if any(v.url == video.url for v in self._videos):
      return False
    if validate_url(video.url):
      self._videos.append(video)
      self.list_changed.emit()
      return True
    return False

  def remove_video(self, url: str) -> None:
    self._videos = [v for v in self._videos if v.url != url]

  def get_first(self) -> str:
    if self._videos:
      return self._videos[0]
    return ""

  def get_last(self) -> str:
     if self._videos:
        return self._videos[-1]
     return ""

  def get_all(self) -> list[VideoData]:
    if self._videos:
        return self._videos
    return []

  def clear_all(self) -> None:
    self._videos = []

  def get_by_url(self, url: str) -> VideoData | None:
    return next((v for v in self._videos if v.url == url), None)
