from typing import List

from PyQt5.QtCore import pyqtSlot, QAbstractAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, \
    QPropertyAnimation, Qt
from PyQt5.QtWidgets import QSizePolicy, QStackedWidget, QWidget


class HStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super(HStackedWidget, self).__init__(parent)

        self._slide_direction = Qt.Horizontal
        self._slide_speed = 500
        self._animation_type = QEasingCurve.OutCubic
        self._cur_idx = 0
        self._next_idx = 0
        self._wrap = False
        self._pos_current = QPoint(0, 0)
        self._active = False
        self._widgets = []

    def set_direction(self, direction) -> None:
        self._slide_direction = direction

    def set_speed(self, speed) -> None:
        self._slide_speed = speed

    def set_animation(self, animation_type) -> None:
        self._animation_type = animation_type

    def set_wrap(self, wrap) -> None:
        self._wrap = wrap

    def widgets(self) -> List[QWidget]:
        return self._widgets

    def addWidget(self, widget: QWidget) -> int:
        widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._widgets.append(widget)
        return super().addWidget(widget)

    def setCurrentIndex(self, index: int) -> None:
        super().setCurrentIndex(index)
        self._show_current_widget()

    @pyqtSlot()
    def slide_previous(self) -> None:
        now = self.currentIndex()
        if self._wrap or now > 0:
            self.slide_to_index(now - 1)

    @pyqtSlot()
    def slide_next(self) -> None:
        now = self.currentIndex()
        if self._wrap or now < (self.count() - 1):
            self.slide_to_index(now + 1)

    def slide_to_index(self, idx: int) -> None:
        if idx != 0:
            if idx > (self.count() - 1):
                idx %= self.count()
            elif idx < 0:
                idx = (idx + self.count()) % self.count()
        self.slide_to_widget(self.widget(idx))

    def slide_to_widget(self, widget: QWidget) -> None:
        if self._active:
            return

        self._active = True

        idx = self.currentIndex()
        next_idx = self.indexOf(widget)

        if idx == next_idx:
            self._active = False
            return

        offset_x, offset_y = self.frameRect().width(), self.frameRect().height()
        self.widget(next_idx).setGeometry(self.frameRect())

        if not self._slide_direction == Qt.Horizontal:
            if idx < next_idx:
                offset_x, offset_y = 0, -offset_y
            else:
                offset_x = 0
        else:
            if idx < next_idx:
                offset_x, offset_y = -offset_x, 0
            else:
                offset_y = 0

        pos_next = self.widget(next_idx).pos()
        pos_current = self.widget(idx).pos()
        self._pos_current = pos_current

        offset = QPoint(offset_x, offset_y)
        self.widget(next_idx).move(pos_next - offset)
        self.widget(next_idx).show()
        self.widget(next_idx).raise_()

        anim_group = QParallelAnimationGroup(self, finished=self.animation_done)

        for index, start, end in zip(
            (idx, next_idx), (pos_current, pos_next - offset), (pos_current + offset, pos_next)
        ):
            animation = QPropertyAnimation(
                self.widget(index),
                b"pos",
                duration=self._slide_speed,
                easingCurve=self._animation_type,
                startValue=start,
                endValue=end,
            )
            anim_group.addAnimation(animation)

        self._next_idx = next_idx
        self._cur_idx = idx
        self._active = True
        anim_group.start(QAbstractAnimation.DeleteWhenStopped)

    @pyqtSlot()
    def animation_done(self) -> None:
        self.setCurrentIndex(self._next_idx)
        self.widget(self._cur_idx).hide()
        self.widget(self._cur_idx).move(self._pos_current)
        self._active = False
        self._show_current_widget()

    def _show_current_widget(self):
        for idx, widget in enumerate(self._widgets):
            if idx == self.currentIndex():
                widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
                widget.adjustSize()
                widget.show()
            else:
                widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
                widget.hide()
        self.adjustSize()
        self.updateGeometry()
