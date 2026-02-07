import sys
import traceback
from types import TracebackType
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThreadPool
from yt_dlp_gui.ui.main_ui import UI
from yt_dlp_gui.mvc.url_store import URLStore

def exceptiom_hook(exctype: type, value: BaseException, tb: TracebackType) -> None:
  error_msg = "".join(traceback.format_exception(exctype, value, tb))

  msg = QMessageBox()
  msg.setIcon(QMessageBox.Icon.Critical)
  msg.setText("An unexpected error occured.")
  msg.setInformativeText(str(value))
  msg.setDetailedText(error_msg)
  msg.setWindowTitle("App error")
  msg.exec()

def main_app() -> int:
  sys.excepthook = exceptiom_hook
  app = QApplication()
  app.setWindowIcon(QIcon(":/icons/app_icon.ico"))
  app.setStyle("Fusion")

  pool = QThreadPool.globalInstance()
  pool.setMaxThreadCount(1)

  store = URLStore()

  window = UI(url_store=store, thread_pool=pool)
  window.show()

  return app.exec()

if __name__ == "__main__":
  sys.exit(main_app())

