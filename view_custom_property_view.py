# view_cal_cell_property.py
# This is to customize what content is rendered at 
# view_main's calendar view

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout,
     QWidget, QLabel, 
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt 

class CustomPropertyViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        pass