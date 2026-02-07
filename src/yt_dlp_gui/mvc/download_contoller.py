from yt_dlp_gui.mvc.url_store import URLStore
from yt_dlp_gui.utils.models import VideoData, SelectionState

class DownloadController:
  def __init__(self, store: URLStore) -> None:
    self.store = store

  def prepare_and_add_video(self, url: str, menu_state: SelectionState) -> bool:
    if menu_state.is_opus:
      ext = "opus"
      res = "None"
      format_id = "bestaudio[acodec=opus]/bestaudio"
    else:
      if not menu_state.res or not menu_state.ext:
        return False
      ext = menu_state.ext
      res = menu_state.res
      format_id = menu_state.format_id

    new_entry = VideoData(
      url = url,
      extension=ext,
      resolution=res,
      subtitles=menu_state.subtitles,
      thumbnail=menu_state.thumbnail,
      metadata=menu_state.metadata,
      format_id=format_id,
    )

    return self.store.add_video(new_entry)