import yt_dlp

profiles = {
  "audio_opus": {
    "format": "bestaudio[codec=opus]/bestaudio",
  },
}

class Downloader:
  def __init__(self, mode: str, url : str) -> None:
    self.url = url
    self.mode = mode
    self.opts = {
      "format": "bestvideo+bestaudio/best",
      "outtmpl": "%(title)s.%(ext)s",
      "writethumbnail": True,
      "postprocessors": [
        {
          "key": "FFmpegExtractAudio",
          "preferredcodec": "opus",
        },
        {
          "key": "FFmpegThumbnailsConvertor",
          "format": "jpg",
        },
        {
          "key": "FFmpegMetadata",
          "add_metadata": True,
        },
        {
          "key": "EmbedThumbnail",
        },
      ],
    }
    self._apply_profile()

  def _apply_profile(self) -> None:
    if self.mode in profiles:
      self.opts.update(profiles[self.mode])

  def download(self) -> None:
    with yt_dlp.YoutubeDL(self.opts) as ydl:
      ydl.download([self.url])


