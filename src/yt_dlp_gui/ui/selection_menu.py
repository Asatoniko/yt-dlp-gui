from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel, QVBoxLayout, QCheckBox

class SelectionMenu(QWidget):
  _layout: QHBoxLayout

  def __init__(self) -> None:
    super().__init__()
    self._all_formats = []
    self._layout = QHBoxLayout(self)

    self._create_left_menu()
    self._create_checkables()
    self._set_selectors()

    self._layout.addWidget(self._left_widget)
    self._layout.addWidget(self._checkables_widget)

  def _create_left_menu(self) -> None:
    self._left_widget = QWidget()
    self._left_layout = QVBoxLayout(self._left_widget)
    self._res_ext_layout = QHBoxLayout()

    self._create_res_widget()
    self._create_ext_widget()
    self._create_opus_checkbox()

    self._left_layout.addWidget(self.opus_checkbox)
    self._res_ext_layout.addWidget(self._res_widget)
    self._res_ext_layout.addWidget(self._ext_widget)
    self._left_layout.addLayout(self._res_ext_layout)

  def _create_opus_checkbox(self) -> None:
    self.opus_checkbox = QCheckBox("Download in .opus format")

  def _create_res_widget(self) -> None:
    self._res_widget = QWidget()
    self._res_layout = QVBoxLayout(self._res_widget)
    res_label = QLabel("Resolution")
    self.res_combo = QComboBox()
    self._res_layout.addWidget(res_label)
    self._res_layout.addWidget(self.res_combo)
    self.res_combo.currentTextChanged.connect(self._filter_formats)

  def _create_ext_widget(self) -> None:
    self._ext_widget = QWidget()
    self._ext_layout = QVBoxLayout(self._ext_widget)
    ext_label = QLabel("Extention")
    self.ext_combo = QComboBox()
    self._ext_layout.addWidget(ext_label)
    self._ext_layout.addWidget(self.ext_combo)

  def _create_checkables(self) -> None:
    self._checkables_widget = QWidget()
    self._checkables_layout = QVBoxLayout(self._checkables_widget)
    self.subtitles = QCheckBox("Subtitles")
    self.thumbnail = QCheckBox("Embed thumbnail")
    self.add_metadata  = QCheckBox("Add metadata")
    self._checkables_layout.addWidget(self.subtitles)
    self._checkables_layout.addWidget(self.thumbnail)
    self._checkables_layout.addWidget(self.add_metadata)

  def _set_selectors(self) -> None:
    self.opus_checkbox.setProperty("class", "selection_box")
    self.subtitles.setProperty("class", "selection_box")
    self.thumbnail.setProperty("class", "selection_box")
    self.add_metadata.setProperty("class", "selection_box")

  def _filter_formats(self, selected_quality: str) -> None:
    self.ext_combo.clear()
    extensions = set()
    for f in self._all_formats:
      res = f.get("resolution") or f.get("format_note", "N/A")
      if res == selected_quality:
        ext = f.get("ext", "N/A")
        if ext not in extensions:
          f_id = f.get("format_id")
          self.ext_combo.addItem(ext, f_id)
          extensions.add(ext)

  def set_data(self, info_dict: dict) -> None:
    self._all_formats = info_dict.get("formats", [])

    subtitles_b = bool(info_dict.get("subtitles"))
    thumbnail_b = bool(info_dict.get("thumbnail"))
    self.subtitles.setEnabled(subtitles_b)
    self.thumbnail.setEnabled(thumbnail_b)

    self.res_combo.blockSignals(True) #noqa: FBT003
    self.res_combo.clear()
    unique_res = {
      f.get("resolution") or f.get("format_note", "N/A")
      for f in self._all_formats
      if f.get("vcodec") != "none"
    }

    resolutions = sorted(unique_res, reverse=True)
    self.res_combo.addItems(resolutions)
    self.res_combo.blockSignals(False) #noqa: FBT003
    self._filter_formats(self.res_combo.currentText())

  def reset_ui(self) -> None:
    self.res_combo.clear()
    self.ext_combo.clear()
    self.thumbnail.setEnabled(True)
    self.subtitles.setEnabled(True)