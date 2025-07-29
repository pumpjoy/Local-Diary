from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QFontMetrics
from PyQt6.QtCore import Qt, QPoint

class CalendarCellWidget(QLabel):
    def __init__(self, text="", is_today=False, *args, **kwargs):
        super().__init__("", *args, **kwargs)  # Don't pass text to QLabel
        self.display_text = text
        self.is_today = is_today
        self.margin = 8  # Margin from top-left

    def set_today(self, is_today):
        self.is_today = is_today 

    def setText(self, text):
        self.display_text = text 

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        font = self.font()
        metrics = QFontMetrics(font)
        x = self.margin
        y = self.margin + metrics.ascent()

        # Draw the number
        painter.setPen(QColor(self.palette().color(self.foregroundRole())))
        painter.drawText(x, y, self.display_text)

        # If today, draw a circle around the number
        if self.is_today:
            # Get bounding rect for the text
            text_rect = metrics.boundingRect(self.display_text)
            # Adjust position to where text is drawn
            text_rect.moveTopLeft(QPoint(x, self.margin))
            # Calculate center of the bounding rect
            center_x = text_rect.left() + text_rect.width() // 2 + 1
            center_y = text_rect.top() + text_rect.height() // 2 + 1
            # Circle radius with padding
            radius = max(text_rect.width(), text_rect.height()) // 2 + 6
            pen = QPen(QColor("red"), 2)
            painter.setPen(pen)
            painter.drawEllipse(QPoint(center_x, center_y), radius, radius)