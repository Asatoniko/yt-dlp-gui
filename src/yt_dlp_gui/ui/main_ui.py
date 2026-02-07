from PySide6.QtCore import QThreadPool, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QMessageBox
from PySide6.QtGui import QMouseEvent
from yt_dlp_gui.mvc.url_store import URLStore
from yt_dlp_gui.ui.themes import engine
from yt_dlp_gui.ui.input_section import UrlInput
from yt_dlp_gui.ui.selection_menu import SelectionMenu
from yt_dlp_gui.ui.directory_picker import DirectoryPicker
from yt_dlp_gui.ui.buttons import Buttons
from yt_dlp_gui.ui.progress_bar import ProgressBar
from yt_dlp_gui.ui.video_list import VideoList
from yt_dlp_gui.utils.utils import validate_url
from yt_dlp_gui.utils.models import VideoData, SelectionState
from yt_dlp_gui.mvc.download_processor import DownloadProcessor
from yt_dlp_gui.mvc.search_worker import SearchWorker
from yt_dlp_gui.utils.models import DownloadDetails
from yt_dlp_gui.mvc.download_contoller import DownloadController

class UI(QWidget):
  def __init__(self, url_store: URLStore, thread_pool: QThreadPool) -> None:
    super().__init__()
    self.url_store = url_store
    self._pool = thread_pool

    self.setMinimumSize(600, 600)
    self.setWindowTitle("yt-gui")
    self.is_dark = False

    self._setup_ui()

    videos = self.url_store.get_all()
    self._video_list.sync_with_store(videos)

  def mousePressEvent(self, event: QMouseEvent) -> None: #noqa: N802
    focused = QApplication.focusWidget()
    if focused:
      focused.clearFocus()
    super().mousePressEvent(event)

  def _setup_ui(self) -> None:
    self.main_layout = QVBoxLayout(self)
    self._create_elements()
    self._layout_elements()
    self._setup_logic()
    self.apply_theme()

  def _create_elements(self) -> None:
    self._input_section = UrlInput()
    self._selection_menu = SelectionMenu()
    self._directory_picker = DirectoryPicker()
    self._button_section = Buttons()
    self._progress_bar = ProgressBar()
    self._video_list = VideoList(self.url_store)
    self._download_controller = DownloadController(self.url_store)

  def _layout_elements(self) -> None:
    widgets = [
      self._input_section, self._selection_menu, self._directory_picker,
      self._button_section, self._progress_bar, self._video_list,
    ]

    for widget in widgets:
      self.main_layout.addWidget(widget)

  def _setup_logic(self) -> None:
    self._selection_menu.opus_checkbox.stateChanged.connect(self._handle_opus_checkbox)
    self._button_section.change_theme.connect(self.switch_theme)

    self._button_section.download_all.connect(self._handle_download_all)
    self._button_section.remove_all.connect(lambda: (
      self.url_store.clear_all(),
      self._video_list.sync_with_store([]),
    ))

    self._input_section.url_input.editingFinished.connect(self._validate_input_state)
    self._input_section.add_url.connect(self._handle_add_video)
    self._input_section.search_info.connect(self._handle_search)
    self._video_list.download_clicked.connect(self._proceed_download)

  def _validate_input_state(self) -> None:
    url = self._input_section.url_input.text()
    is_valid = validate_url(url)
    self._input_section.search_button.setEnabled(is_valid)

  def _handle_opus_checkbox(self, state: int) -> None:
    if state == Qt.CheckState.Checked.value:
      self._input_section.search_button.setEnabled(False)
    else:
      self._input_section.search_button.setEnabled(True)

  def _handle_download_all(self) -> None:
    all_videos = self.url_store.get_all()
    for video in all_videos:
      self._proceed_download(video)
    self.url_store.clear_all()
    self._video_list.sync_with_store([])

  def _proceed_download(self, video: VideoData) -> None:
    self._download_path = self._directory_picker.path_display.text()
    processor = DownloadProcessor(video, self._download_path)
    processor.signals.progress_updated.connect(lambda percent: self._progress_bar.update_bar(percent))
    processor.signals.details.connect(self._progress_bar.update_details)
    entry = DownloadDetails(
      title="",
      speed="N/A",
      size="N/A",
      status="Finished",
      time="00:00",
    )
    processor.signals.finished.connect(lambda: self._progress_bar.update_details(entry))
    self._pool.start(processor)

  def _handle_search(self) -> None:
    url = self._input_section.url_input.text()
    if validate_url(url):
      self._input_section.search_button.setEnabled(False)
      worker = SearchWorker(url)

      worker.signals.finished.connect(self._on_search_finished)
      worker.signals.error.connect(self._on_search_failed)

      self._pool.start(worker)

  def _on_search_finished(self, dictionary: dict) -> None:
    self._selection_menu.set_data(dictionary)
    self._input_section.search_button.setEnabled(True)

  def _on_search_failed(self, error_msg: str) -> None:
    self._input_section.search_button.setEnabled(True)
    self._progress_bar.set_status(f"Error: {error_msg}", color="red")
    QMessageBox.critical(self, "Search Failed", f"Could not fetch video info:\n{error_msg}")

  def _handle_add_video(self) -> None:
    url = self._input_section.url_input.text()

    raw_state = SelectionState(
      is_opus = self._selection_menu.opus_checkbox.isChecked(),
      res = self._selection_menu.res_combo.currentText(),
      ext = self._selection_menu.ext_combo.currentText(),
      format_id = self._selection_menu.ext_combo.currentData(), # if opus, id is changed further in the controller
      subtitles = self._selection_menu.subtitles.isChecked(),
      thumbnail = self._selection_menu.thumbnail.isChecked(),
      metadata = self._selection_menu.add_metadata.isChecked(),
    )

    success = self._download_controller.prepare_and_add_video(url, raw_state)

    if success:
      self._input_section.url_input.clear()
      self._selection_menu.reset_ui()
      self._video_list.sync_with_store(self.url_store.get_all())

  def switch_theme(self) -> None:
    self.is_dark = not self.is_dark
    self.apply_theme()

  def apply_theme(self) -> None:
    theme = "dark" if self.is_dark else "light"
    style = engine.load_stylesheet(theme)
    QApplication.instance().setStyleSheet(style)

