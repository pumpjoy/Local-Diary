from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout,
     QWidget, QLabel, 
)
from PyQt6.QtGui import QPainter, QPen, QColor, QFontMetrics
from PyQt6.QtCore import Qt, QPoint

from asset.css_cheatsheet import(
    GLOBAL_CAL_HEAD_MARGIN,
)

class CalendarCellWidget(QWidget):
    def __init__(self, text="", is_today=False, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        
        self.date_label_margin = 8

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self) 
        self.main_layout.setContentsMargins(0, 0, 0, 0) 

        # Create a QHBoxLayout
        self.is_today = is_today
        self.date_label = QLabel(text=text) 
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.date_label.setMargin(4)  # Set date_label_margin for the label   

        self.main_layout.addWidget(self.date_label)
        self.main_layout.stretch(1)

    def cus_set_text(self, text):
        self.date_label.setText(text)

    def set_today(self, is_today): 
        self.is_today = is_today

    def today_style(self, style):
        self.date_label.setStyleSheet(style)

class CalendarHeaderWidget(QWidget):
    # TODO: Stays a widget until further actions
    # Should be a label
    def __init__(self, text="", *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_layout = QVBoxLayout(self) 
        self.main_layout.setContentsMargins(0, 0, 0, 0) 
        self.day_label = QLabel(text=text) 
        self.day_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.day_label.setMargin(GLOBAL_CAL_HEAD_MARGIN)
        self.main_layout.addWidget(self.day_label)
        self.main_layout.stretch(1)
    
    def cus_set_text(self, text):
        self.day_label.setText(text)