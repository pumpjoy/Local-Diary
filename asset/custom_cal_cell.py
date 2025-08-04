import datetime
from PyQt6.QtWidgets import (
    QSizePolicy,
    QGroupBox, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QPushButton,
) 
from PyQt6.QtCore import Qt 

from helper.diary_property_manager import DiaryPropertyConfiguration

from asset.css_cheatsheet import(
    GLOBAL_CAL_HEAD_MARGIN,
)

class CalendarCellWidget(QWidget):
    def __init__(self, dateis="", full_date:datetime=None, is_today=False, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        
        self.is_today = is_today 
        self.date_label_margin = 4
        self.bt_add_new_entry_margin = 4
        self.full_date=full_date.strftime('%Y-%m-%d') 

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.parent_layout = QVBoxLayout(self)
        self.parent_layout.setContentsMargins(0, 0, 0, 0)
        self.parent_layout.setSpacing(0)
        self.main_layout = QGroupBox(self) 
        self.parent_layout.addWidget(self.main_layout)

        self.content_layout = QVBoxLayout(self.main_layout)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # Date number header
        # Horizontal layout for bt_add_new_entry + date_label
        header_h_layout = QHBoxLayout()
        header_h_layout.setContentsMargins(0, 0, 0, 0) 
        header_h_layout.setSpacing(0) 
        
        self.bt_add_new_entry = QPushButton('+') # Placeholder for button  
        self.bt_add_new_entry.setToolTip("Add new entry")
        self.bt_add_new_entry.setCursor(Qt.CursorShape.CrossCursor)
        self.bt_add_new_entry.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.bt_add_new_entry.setStyleSheet(f"margin: {self.bt_add_new_entry_margin}px;")
        self.bt_add_new_entry.setFixedSize(30, 30) 
        self.bt_add_new_entry.clicked.connect(self._add_new_entry)
        
        self.date_label = QLabel(text=dateis) 
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)   
        self.date_label.setStyleSheet(f"border: 1px solid transparent; background: transparent; margin: {self.date_label_margin}px;")

        header_h_layout.addWidget(self.bt_add_new_entry)
        header_h_layout.addStretch(1)
        header_h_layout.addWidget(self.date_label) 
        
        self.content_layout.addLayout(header_h_layout) 
        self.content_layout.addStretch(1)
 

        # --- Actual content --- 
        # Get from json



    def cus_set_text(self, text):
        self.date_label.setText(text)

    def set_today(self, is_today): 
        self.is_today = is_today

    def today_style(self, style):
        self.date_label.setStyleSheet(style)


    def _add_new_entry(self):
        from PyQt6.QtWidgets import QMessageBox
        try:
            import shutil
            """Adds new entry date.json based on template."""
            self.diary_config = DiaryPropertyConfiguration()
            template_path = self.diary_config.change_mode(edit_mode=True) 
            entry_path = self.diary_config.change_mode(edit_mode=False, date=self.full_date)
            print(f"template_path = {template_path}")
            print(f"entry_path = {entry_path}")
            shutil.copy(template_path, entry_path)
            # QMessageBox.information(None, "Success", f"Template successfully copied and renamed to {entry_path}")
            # NEW: tell view_main to reload this specific view
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")

class CalendarHeaderWidget(QWidget):
    # FUTURE: Stays a widget until further actions
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