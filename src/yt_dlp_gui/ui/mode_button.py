from PySide6.QtWidgets import QAbstractButton, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, Property, QEasingCurve, QPoint, QRect
from PySide6.QtGui import QPainter, QColor
from yt_dlp_gui.utils.utils import render_svg

class ModeButton(QAbstractButton):
  def __init__(self, parent: QWidget | None=None, *, width: int = 200) -> None:
    super().__init__(parent)
    self.width = width
    self.height = width // 2
    self.setFixedSize(self.width, self.height)
    self.setCheckable(True)
    self._icon_size = self.width * 0.375
    self._ellipse_x = self.width * 0.25
    self._end = self.width * 0.735
    self._start = self.width * 0.25
    self._rounding = self.width * 0.075
    self._el_h = self.width * 0.25
    self._radius = self.height*0.42

    self._icon_moon = render_svg(self, ":/icons/moon.svg", self._icon_size)
    self._icon_sun = render_svg(self, ":/icons/sun.svg", self._icon_size)

    self._anim = QPropertyAnimation(self, b"ellipse_x")
    self._anim.setDuration(350)
    self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

    self.toggled.connect(self._ellipse_transition)

  @Property(int)
  def ellipse_x(self) -> None:
    return self._ellipse_x

  @ellipse_x.setter
  def ellipse_x(self, val: float) -> None:
    self._ellipse_x = val
    self.update()

  def _ellipse_transition(self, _checked: bool) -> None: #noqa: FBT001
    self._anim.stop()
    self._anim.setEndValue(self._end if _checked else self._start)
    self._anim.start()

  def nextCheckState(self) -> None: #noqa: N802
    return super().nextCheckState()

  def paintEvent(self, _event) -> None: #noqa: N802, ANN001
    painter = QPainter(self)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    bg = QColor("#C7DBDE") if self.isChecked() else QColor("#D5DA52")
    painter.setBrush(bg)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, self.width, self.height, self._rounding, self._rounding)

    margin = self._rounding
    left_rect = QRect(margin, 0, self._icon_size, self.height)
    self.style().drawItemPixmap(painter, left_rect, Qt.AlignmentFlag.AlignCenter, self._icon_moon)

    right_rect = QRect(margin*2+self._icon_size, 0, self._icon_size, self.height)
    self.style().drawItemPixmap(painter, right_rect, Qt.AlignmentFlag.AlignCenter, self._icon_sun)

    painter.setBrush("white")
    painter.drawEllipse(QPoint(self._ellipse_x, self._el_h), self._radius, self._radius)
