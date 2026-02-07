from dataclasses import dataclass

@dataclass
class VideoData:
  url: str
  extension: str
  resolution: str
  subtitles: bool
  thumbnail: bool
  metadata: bool
  format_id: str

@dataclass
class DownloadDetails:
  title: str
  speed: str
  size: str
  status: str
  time: str

@dataclass
class SelectionState:
  is_opus: bool
  res: str
  ext: str
  format_id: str
  subtitles: bool
  thumbnail: bool
  metadata: bool