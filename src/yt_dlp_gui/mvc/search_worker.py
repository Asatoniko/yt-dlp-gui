import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
from PySide6.QtCore import QObject, Signal, QRunnable, Slot

class SearchSignals(QObject):
  finished = Signal(dict)
  error = Signal(str)

class SearchWorker(QRunnable):
  def __init__(self, url: str) -> None:
    super().__init__()
    self.url = url
    self.signals = SearchSignals()

  @Slot()
  def run(self) -> None:
    try:
      opts = {}
      with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(self.url, download=False)
        self.signals.finished.emit(info)
    except (DownloadError,ExtractorError) as e:
      self.signals.error.emit(str(e))