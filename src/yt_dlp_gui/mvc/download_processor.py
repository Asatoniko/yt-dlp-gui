import re
from pathlib import Path
from PySide6.QtCore import QRunnable, Slot, QObject, Signal
from yt_dlp_gui.utils.models import VideoData
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
from yt_dlp_gui.utils.models import DownloadDetails

class ProgressSignals(QObject):
  progress_updated = Signal(int)
  details = Signal(DownloadDetails) #title, speed, size, status, time
  finished = Signal()

def clean_ansi(text: str) -> str:
  return re.sub(r"(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]", "", text).strip()

class DownloadProcessor(QRunnable):
  def __init__(self, video_data: VideoData, path: str) -> None:
    super().__init__()
    self.video_data = video_data
    self._path = path
    self.signals = ProgressSignals()

  @Slot()
  def run(self) -> None:
    format_str = "bestaudio[acodec=opus]/bestaudio" if self.video_data.extension == "opus" else f"{self.video_data.format_id}+bestaudio/best" #noqa: E501

    opts = {
      "format": format_str,
      "writethumbnails": self.video_data.thumbnail,
      "writesubtitles": self.video_data.subtitles,
      "writeautomaticsub": self.video_data.subtitles,
      "addmetadata": self.video_data.metadata,
      "xattrs": self.video_data.metadata,
      "outtmpl": f"{self._path}/%(title)s.%(ext)s",
      "postprocessors": [],
      "nocolor": True,
      "progress_hooks": [lambda dictionary: progress_hook(dictionary, self)],
    }

    if self.video_data.thumbnail:
      opts["postprocessors"].append({
        "key": "EmbedThumbnail",
        "already_have_thumbnail": False,
      })

    if self.video_data.extension == "opus":
      opts["postprocessors"].append({
        "key": "FFmpegExtractAudio",
        "preferredcodec": "opus",
      })

    if self.video_data.metadata:
      opts["postprocessors"].append({
        "key": "FFmpegMetadata",
        "add_chapters": True,
        "add_metadata": True,
      })

    try:
      with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([self.video_data.url])
    except (DownloadError,ExtractorError):
      pass

def progress_hook(d: dict, processor: DownloadProcessor) -> None:
  signals = processor.signals
  title = processor.video_data.url

  if "filename" in d:
    title = Path(d["filename"]).stem

  if d["status"] == "downloading":
    percent_str = clean_ansi(d.get("_percent_str", "0")).replace("%", "".strip())
    estimated_time = clean_ansi(d.get("_eta_str", "N/A"))
    speed = clean_ansi(d.get("_speed_str", "N/A"))
    size = clean_ansi(d.get("_total_bytes_str", "N/A"))

    if len(estimated_time) > 5 and " " in estimated_time: #noqa: PLR2004
      estimated_time = estimated_time.split(" ")[-1]

    try:
      percent = int(float(percent_str))
      signals.progress_updated.emit(percent)
      entry = DownloadDetails(
        title=title,
        speed=speed,
        size=size,
        status="Downloading",
        time=estimated_time,
      )
      signals.details.emit(entry)
    except ValueError:
      pass

  elif d["status"] == "finished":
    signals.progress_updated.emit(100)
    signals.finished.emit()