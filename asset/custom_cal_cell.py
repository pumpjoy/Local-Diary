import os

import datetime
from PyQt6.QtWidgets import (
    QSizePolicy,
    QGroupBox, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QPushButton,
) 
from PyQt6.QtCore import Qt, QSize

from asset.css_cheatsheet import(
    MAIN_PAGE_CAL_HEAD_MARGIN,
)

class CalendarCellWidget(QWidget):
 
    def __init__(self, diary_config, widthis, dateis="", full_date:datetime=None, is_today=False, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.diary_config = diary_config  
        self.full_date=full_date.strftime('%Y-%m-%d')  
        self.is_today = is_today 
        self.date_label_margin = 4
        self.bt_add_new_entry_margin = 4

        self.setMinimumWidth(widthis)
        self.setSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Minimum)


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
        self.bt_add_new_entry.setFixedSize(30, 30) 
        self.bt_add_new_entry.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.bt_add_new_entry.setStyleSheet(f"margin: {self.bt_add_new_entry_margin}px;")
        self.bt_add_new_entry.clicked.connect(self._add_new_entry)
        
        self.date_label = QLabel(text=dateis) 
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)   
        self.date_label.setStyleSheet(f"border: 1px solid transparent; background: transparent; margin: {self.date_label_margin}px;")


        header_h_layout.addWidget(self.bt_add_new_entry)
        header_h_layout.addStretch(1)
        header_h_layout.addWidget(self.date_label) 
        
        
        # --- Display the properties for this date --- 
        # Temporary, will just show their stats
        self.v_property_render = QVBoxLayout()
        self.v_property_render.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.v_property_render.setContentsMargins(0, 0, 0, 0) 
        self.v_property_render.setSpacing(0) 
        # Get and render entry based on date
        self._render_entry() 
        self.v_property_render.addStretch(1)

        # --- End ---
        self.content_layout.addLayout(header_h_layout)   
        self.content_layout.addLayout(self.v_property_render)  
        self.content_layout.addStretch(1)
 
        # self.setMinimumHeight(self.sizeHint().height())
  
    def cus_set_text(self, text):
        self.date_label.setText(text)

    def set_today(self, is_today): 
        self.is_today = is_today

    def today_style(self, style):
        self.date_label.setStyleSheet(style)
  

    def _add_new_entry(self):
        from PyQt6.QtWidgets import QMessageBox
        try:
            import re
            import shutil
            from pathlib import Path
            """
            Adds new entry date.json based on template. 
            Has built in duplication checks.
            Ensures existing data must never get overwritten."""
            template_path = self.diary_config.change_mode(edit_mode=True) 
            entry_path = self.diary_config.change_mode(edit_mode=False, date=self.full_date)
            # Check if file name exists
            if os.path.isfile(entry_path):
                print("File path exists.")
                # Check if has (1) behind it; check if it already has a copy
                entry_path = Path(entry_path)
                dir_path = entry_path.parent
                file_stem = entry_path.stem # entry_2025-08-05
                file_suffix = entry_path.suffix # .json

                glob_pattern = f"{file_stem}*{file_suffix}"
                number_pattern = re.compile(r"\((?P<number>\d+)\)")
                existing_numbers = [] 
                
                for file in dir_path.glob(glob_pattern): 
                    filename_stem = file.stem
                    # Search for (number)
                    match = number_pattern.search(filename_stem) 
                    if match: 
                        # If number is found, add to list
                        number = int(match.group('number'))
                        existing_numbers.append(number)
                    else: 
                        # If the filename stem is exactly the base stem, 
                        # it's the un-numbered file.
                        if filename_stem == file.stem:
                            existing_numbers.append(0)

                if not existing_numbers:
                    next_number = 1
                else: 
                    max_number = max(existing_numbers)
                    next_number = max_number + 1

                entry_path = f"{file_stem}({next_number}){file_suffix}"
                entry_path = dir_path / entry_path


            """else: create a new file as per default"""
            shutil.copy(template_path, entry_path)
            # QMessageBox.information(None, "Success", f"Template successfully copied and renamed to {entry_path}")
            self._render_entry()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")

    def _render_entry(self):
        print("Rendering entry............")
        entry_path = self.diary_config.change_mode(edit_mode=False, date=self.full_date)
        if os.path.isfile(entry_path): 
            print(f"Entry for {self.full_date} found.") 
            
            title = self.diary_config.get_setting('title', [])
            date = self.diary_config.get_setting('date', []) # TODO: fill this date automatically #TODO: date changes name of file! make sure to add index!
            load_data = self.diary_config.get_setting('dynamic_rows', [])
            
            self.next_row_id = 0

            if load_data:
                # Render by property_type
                for row_data in load_data:
                    property_key = row_data.get(f"property_key", "Loaded Item")
                    property_type = row_data.get("property_type", "text")
                    property_value = row_data.get("property_value", "No Data Loaded")
                    label = self._render_properties(
                        property_key=property_key, property_type=property_type,property_value=property_value)
                    self.v_property_render.addWidget(label)
            else:
                print("No dynamic rows (template) found in config. Starting with an empty template.")

            # Render individual based on property_type
            # for row_data in 
    
    def _render_properties(self, property_key="", property_type="text", property_value="Unknown type. Default to text"):
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        label.setWordWrap(False)
        label.setStyleSheet(f"border: 1px solid transparent; background: transparent;")

        match property_type:
            case "text" | "number":
                label.setText(property_value)
                print(property_type)
                return label 
            case "select":
                label.setText(property_value)
                print(property_type)
                return label 
            case "multi_select":
                label.setText(property_value)
                print(property_type)
                return label 
            case "status":
                label.setText(property_value)
                print(property_type)
                return label 
            case "checkbox":
                label.setText(property_value)
                print(property_type)
                return label 

class CalendarHeaderWidget(QWidget):
    # FUTURE: Stays a widget until further actions
    # Should be a label
    def __init__(self, text="", horizontal_policy=None, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.setSizePolicy(horizontal_policy, QSizePolicy.Policy.Preferred)
        self.main_layout = QVBoxLayout(self) 
        self.main_layout.setContentsMargins(0, 0, 0, 0) 
        self.day_label = QLabel(text=text) 
        self.day_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.day_label.setMargin(MAIN_PAGE_CAL_HEAD_MARGIN)
        self.main_layout.addWidget(self.day_label)
        self.main_layout.stretch(1)
    
    def cus_set_text(self, text):
        self.day_label.setText(text)
    
    def get_width(self):
        """Gets width of CalendarHeaderWidget for row!=0 renders"""
        return self.sizeHint().width()