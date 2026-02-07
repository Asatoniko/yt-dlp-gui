from urllib.parse import urlparse
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt, QObject

def render_svg(item: QObject, path: str, icon_size: float) -> QPixmap:
  dpr = item.devicePixelRatioF()
  render_size = int(icon_size * dpr)
  renderer = QSvgRenderer(path)
  pixmap = QPixmap(render_size, render_size)
  pixmap.fill(Qt.GlobalColor.transparent)

  painter = QPainter(pixmap)
  pixmap.setDevicePixelRatio(dpr)
  renderer.render(painter)
  painter.end()
  return pixmap

def validate_url(url: str) -> bool:
    url = url.strip()
    max_len = 50
    if not url.lower().startswith("https://") or len(url) > max_len:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme == "https", result.netloc])
    except ValueError:
        return False
