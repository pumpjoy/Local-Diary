# view_custom_property.py
# To customize one's diary property
# Title and date must exist

# TODO: Will be reused to view individual day content

import os
import datetime
import ast
import json

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QToolButton, QLabel, QLineEdit, QPushButton, QDateEdit, 
    QScrollArea, QMenu, QMessageBox,
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QDate

from asset.custom_row_widget import CustomRowWidget

from asset.css_cheatsheet import (
    MAIN_LABEL_LIGHT_QSS, MAIN_LABEL_DARK_QSS,
    BT_BACK_TO_MAIN_SIZE,
    TYPES_OF_PROPERTIES 
)

from helper.diary_property_manager import DiaryPropertyConfiguration

# --- Custom Property Widget ---
class CustomPropertyWidget(QWidget):
    """ Actually a view"""
    reqeusted_back_to_main = pyqtSignal() 

    def __init__(self, config_manager, parent=None, edit_mode=False, date=None):
        """
        Initializes the CustomPropertyWidget.
        @param config_manager: Instance of DiaryPropertyConfiguration for managing settings.
        @param diary_manager: Instance of DiaryPropertyManager for managing diary entries.
        @param parent: Parent widget, if any.
        @param edit_mode: Whether the widget is in edit mode (for customizing diary properties).
        @param date: Date to view entries for, if in view mode.
        """
        super().__init__(parent)
        self.date = date # Date to view entries for, if in view mode

        self.config_manager = config_manager # For theme 
        self.diary_manager = DiaryPropertyConfiguration() # Store reference to diary manager 
        self.edit_mode = edit_mode # Whether in edit template mode 

        self._setup_edit_ui()
         
        self._connect_signals()
        self.update_updown_button_states()

    def _setup_edit_ui(self):
        """
        Template editing UI setup.
        This is used when the widget is in edit mode. (Customize Diary Property)
        """
        # Main Layout
        page_mainv_layout = QVBoxLayout(self)
        page_mainv_layout.setContentsMargins(15, 15, 15, 15)
        page_mainv_layout.setSpacing(5)

        ### Header 1: Header and Back button
        page_header_h_layout = QHBoxLayout() 
        self.main_label = QLabel()
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter) 
        self.bt_back_to_main = QPushButton("Back to Main")
        self.bt_back_to_main.setFixedSize(*BT_BACK_TO_MAIN_SIZE)
        page_header_h_layout.addWidget(self.main_label, 1)
        page_header_h_layout.addWidget(self.bt_back_to_main)

        ### Header 2: Title and Date
        self.title_label = QLabel("Title") # TODO: Add StyleSheet 
        self.title_edit = QLineEdit()
        self.date_label = QLabel("Date") 
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate()) 
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setEnabled(False) # During Template View, Not editable  

        self.title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.date_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        # Header Grid
        # Initialized early to take into consideration of dynamic buttons' shenanigans
        self.header_grid = QGridLayout(self)
        self.header_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.header_grid.setContentsMargins(0, 0, 0, 0)
        self.header_grid.setSpacing(10)
        
        self.header_grid.addWidget(self.title_label, 0, 0)
        self.header_grid.addWidget(self.title_edit, 0, 1)
        self.header_grid.addWidget(self.date_label, 1, 0)
        self.header_grid.addWidget(self.date_edit, 1, 1)

        ### --- Custom Grid Row Content --- 
        self.grid_scroll_area = QScrollArea(self)
        self.grid_scroll_area.setWidgetResizable(True)
        self.grid_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.grid_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Make Content Grid scrollable
        self.view_scroll_content_widget = QWidget(self.grid_scroll_area)
        self.view_scroll_content_layout = QVBoxLayout(self.view_scroll_content_widget)
        self.view_scroll_content_layout.setContentsMargins(10, 10, 10, 10)
        self.view_scroll_content_layout.setSpacing(10)

        # Actual Grid content
        self.content_grid = QGridLayout()
        # self.content_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_grid.setContentsMargins(0, 0, 0, 0)
        self.content_grid.setSpacing(10)

        self.view_scroll_content_layout.addLayout(self.content_grid)
        self.view_scroll_content_layout.addStretch(1) 

        self.grid_scroll_area.setWidget(self.view_scroll_content_widget)
        

        ### Main Layout filling
        page_mainv_layout.addLayout(page_header_h_layout)  
        page_mainv_layout.addLayout(self.header_grid) 
        page_mainv_layout.addWidget(self.grid_scroll_area, 1)
        page_mainv_layout.stretch(1)

        # Dictionary to store CustomRowWidget instances, mapped by unique row_id
        self.dict_row_widgets = {}
        self.current_row_id = 0 # Counter for generating unique row_ids # Follows row position
        self.add_new_button_widget = None
        self._add_new_row_button()
    
    def load_edit_mode_into_ui(self):
        """
        Loads current diary property settings into the UI widgets.
        This is called when the widget is displayed.
        """ 
        print("CUSTOMPROPERTYWIDGET: LOAD EDIT MODE")
        self.date = None
        self.current_row_id  = 0
        self.edit_mode = True
        self.diary_manager.change_mode(self.edit_mode) 
        self.diary_manager.load_config()
        self.main_label.setText("Customize Diary Property")
        self.title_edit.setText(self.diary_manager.get_setting('title', ''))
        self.date_edit.setDate(QDate.fromString(self.diary_manager.get_setting('date', ''), "dd/MM/yyyy"))
        self._load_custom_row()
        
    def load_view_mode_into_ui(self, date=None):
        """
        Loads current diary property settings into the UI widgets.
        This is called when the widget is displayed.
        """
        print("CUSTOMPROPERTYWIDGET: LOAD VIEW MODE")
        self.date = date
        self.current_row_id  = 0
        self.edit_mode = False
        self.diary_manager.change_mode(edit_mode=self.edit_mode, date=date)
        self.diary_manager.load_config()
        self.main_label.setText(f"Viewing Entry for {date}")
        self.title_edit.setText(self.diary_manager.get_setting('title', ''))
        self.date_edit.setDate(QDate.fromString(self.diary_manager.get_setting('date', ''), "dd/MM/yyyy"))
        self._load_custom_row()


    def _connect_signals(self):
        self.bt_back_to_main.clicked.connect(self._on_bt_back_to_main_clicked)  

    def _on_bt_back_to_main_clicked(self):
        self._save_template()
        self._sync_entries()
        self.reqeusted_back_to_main.emit()
    
    # --- Load and Save Template Logics ---
    def _save_template(self):
        """
        Gathers data from all dynamic rows and saves it as the JSON template
        using the ConfigManager.
        """
        # Actually saving
        data_to_save = []
        ordered_ids = self._get_current_order()

        for row_id in ordered_ids:
            widget = self.dict_row_widgets.get(row_id)
            if widget:
                row_data = {
                    "property_id": widget.property_id,
                    "property_key": widget.property_key.text(),
                    "property_type": widget.property_type,
                    "property_value": widget.property_value
                }
                data_to_save.append(row_data)
        
        self.diary_manager.set_setting('dynamic_rows', data_to_save)
        try:
            self.diary_manager.save_config() 
            # Synchronize the change to template and all entries in this year 
            self._sync_entries()
            # print(f"CustomPropertyWidget: Template saved successfully to {self.diary_manager.config_file_path}")
        except Exception as e:
            print(f"CustomPropertyWidget: Error saving template: {e}")
            print(f"CustomPropertyWidget: Failed to save template to {self.diary_manager.config_file_path}")  

    def _sync_entries(self):
        """
        Synchronizes the entries and template. 
        Note: This only affects entries of THIS YEAR.
        This assumes all checks are done individually by respective functions (delete, change, etc)
        and its job is only to synchronize.
        This is a standalone function meant to do exactly as that.
        """ 

        # 0. Template will check first, if current is template, skip template sync codes
        # 1. Get current widget setup, store the dynamic_row as list;
        # 2. Get files that is not this file, get their list set up.
        # 3. Check the differences by property_id, property_key and property_type
        # 4. Get the difference ones, make changes accordingly (add, delete, move, change type)
        def sync_rows(source_list, target_list, id_key='property_id', type_key = 'property_type'):
            """
            Synchronizes a target list to match a source list based on a unique ID.
            Handles additions, deletions, updates, and reordering.
            @param: source_list (list) The list of dictionaries that is the source of truth.
            @param: target_list (list) The list of dictionaries to be synchronized.
            @param: id_key, type_key (str) The key that holds the unique identifier. 
            @returns: A new list that is fully synchronized with the source list.
            """
            # Create a dictionary for fast lookups of items in the target list
            target_map = {item[id_key]: item for item in target_list if id_key in item}
            synchronized_list = []
    
            # Iterate through the source list to build the new synchronized list
            for source_item in source_list:
                # If item exists in source's id
                # Changes has been done to the property id (that exists)
                if id_key in source_item:
                    source_id = source_item[id_key]

                    # If source id exists in target's id 
                    # This effectively handles `delete_row` actions
                    if source_id in target_map: 
                        target_item = target_map[source_id]

                        # Check if the property_type is the same
                        if source_item.get(type_key) == target_item.get(type_key):
                            # Type unchanged, preserve target's value, change key_key
                            merged_item = source_item.copy()
                            merged_item['property_value'] = target_item.get('property_value')
                            synchronized_list.append(merged_item)
                        else:
                            # Type has changed, we use source item
                            # Reminder: The moment type changes, the value is cleared anyway
                            synchronized_list.append(source_item)
                    else: 
                        # This is a new item, add directly from source
                        # This handles `add_new_row`
                        synchronized_list.append(source_item)

            # The whole thing handles movement changes in row 
            return synchronized_list

        def actually_syncing(entry, edit_mode=False):
            try:
                with open(entry, 'r+', encoding='utf-8') as f:
                    entry_data = json.load(f) 
                    entry_rows = entry_data.get('dynamic_rows', [])  

                    # 3. Check the differences by property_id, property_key and property_type
                    entry_date = entry_data.get('date', "")
                    print(f"ENTRY DATE IS {entry_date}")
                    temp_manager = DiaryPropertyConfiguration()
                    if edit_mode:
                        temp_manager.change_mode(edit_mode=True)
                    else:
                        temp_manager.change_mode(edit_mode=edit_mode, date=entry_date)
                    temp_manager.load_config()
                    updated_rows = sync_rows(current_rows, entry_rows)
                    temp_manager.set_setting('dynamic_rows', updated_rows)
                    temp_manager.save_config()

            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"CustomPropertyWidget: Error getting current file config: {e}")

        # 1. Get current widget setup, store the dynamic_row as list; 
        # This will act as source for others to match
        current_rows = self.diary_manager.get_setting('dynamic_rows', [])   
        
        if self.edit_mode == True:
            print("CUSTOMPROPERTYWIDGET: SYNC: Template Mode")
            # 0. Template will check first, if current is template, skip template sync codes
            # --- Sync to entries --- 
            # Skip template sync codes, go straight to sync-ing entries    
            # 2. Get files that is not this file, get their list set up.
            # Reminder: CHANGE ONLY THIS YEAR!
            
            data_dir = self.diary_manager.get_data_directory(str(datetime.datetime.today().year))
            list_entries = [entry for entry in os.listdir(data_dir)] 
            for entry in list_entries:
                # Because diary_manager.change mode requires known date, and we don't know others' dates
                # Instantly use json.load here  
                entry = os.path.join(data_dir, entry)  
                actually_syncing(entry)
        else: 
            print("CUSTOMPROPERTYWIDGET: SYNC: Entry Mode")
            # Not template mode
            # Entries have changes
            # --- Sync to template ---
            entry = self.diary_manager.get_diary_config_path()
            actually_syncing(entry, edit_mode=True)
            # Change back to current diary_manager 😥
            
            # --- Sync to other entries ---
            data_dir = self.diary_manager.get_data_directory(str(datetime.datetime.today().year))
            list_entries = [entry for entry in os.listdir(data_dir)] 
            for entry in list_entries:
                # Because diary_manager.change mode requires known date, and we don't know others' dates
                # Instantly use json.load here
                
                # Check if entry is self, skip if yes
                print(f"self.date: {self.date}, entry: {entry}")
                if self.date in entry:
                    print("SAME ENTRY SAME ENTRY")
                    continue
                entry = os.path.join(data_dir, entry)  
                actually_syncing(entry)
 

    def _clear_all_rows(self):
        """Helper to clear all DraggableRowWidgets from the grid."""
        current_order_ids = self._get_current_order()
        for row_id in current_order_ids:
            widget = self.dict_row_widgets.pop(row_id, None)
            if widget:
                widget.deleteLater()

    def _load_custom_row(self):
        """
        Loads the dynamic row data (the template) from the config manager
        and populates the grid. Called once on application startup.
        """
        loaded_template_data = self.diary_manager.get_setting('dynamic_rows', [])
        
        self._clear_all_rows() 

        if loaded_template_data:
            print(f"CustomPropertyWidget: Loading {len(loaded_template_data)} dynamic rows (template) from config.")
            for row_data in loaded_template_data:
                property_id = row_data.get("property_id", None)
                property_key = row_data.get("property_key", "Loaded Item")
                property_type = row_data.get("property_type", "text")
                property_value = row_data.get("property_value", "No Data Loaded")
                self._add_new_row(property_id, property_key, property_type, property_value)
        else:
            print("CustomPropertyWidget: No dynamic rows (template) found in config. Starting with an empty template.")
            self._rebuild_layout_from_order([])

        self.update_updown_button_states()

    def _rebuild_layout_from_order(self, new_order_ids: list[int]):
        """
        Clears entire QGridLayout and then re-adds all widgets
        (custom rows and 'Add New' button) in specified new order.
        This ensures visual layout matches logical order.
        """ 
        while self.content_grid.count():
            item = self.content_grid.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None) # Disown widget from layout

        # Re-add CustomRowWidget instances based on new_order_ids list.
        current_grid_row = 0
        for row_id in new_order_ids:
            if row_id in self.dict_row_widgets:
                widget = self.dict_row_widgets[row_id]
                # Add custom row, spanning all available columns
                self.content_grid.addWidget(widget, current_grid_row, 0, 1, self.content_grid.columnCount())
                current_grid_row += 1
        
        # Re-add "Add New" button at the very last row.
        if self.add_new_button_widget:
            self.content_grid.addWidget(self.add_new_button_widget, current_grid_row, 0, 1, self.content_grid.columnCount())
        
        # Prematurely return if only has Add_New
        # Stops it from saving nonsense template (more specifically, final date.json that is empty)
        if self.content_grid.count() == 1: 
            return 

        # Request layout to update itself to reflect changes
        self._save_template()
        self.content_grid.update()

    def update_theme_style(self, theme_name):
        """
        Updates theme-dependent styles of this widget and its children.
        Called by main window.
        """
        if theme_name == 'light': 
            self.main_label.setStyleSheet(MAIN_LABEL_LIGHT_QSS) 
        else: # dark theme 
            self.main_label.setStyleSheet(MAIN_LABEL_DARK_QSS) 

    # --- Dynamic action logic ---     
    def _add_new_row(self,  
                     property_id: str, 
                     property_key: str, 
                     property_type: str, 
                     property_value: str = "", 
                     position: int = None):
        """
        Creates a new CustomRowWidget and adds it to grid.
        This method is called when user clicks "Add New" button.
        new row is always added just above 'Add New' button.
        NEW: Position, to reuse this method during duplication of row.
        @param: position (int) If add new row is not None, adds below position
        """  
        # Changed to follow row position
        row_id = self.current_row_id 

        while row_id in self.dict_row_widgets:
            row_id += 1
        self.current_row_id = row_id + 1
        # self.current_row_id += 1

        # Use row_id as property_id for new rows
        if property_id is None:
            property_id = row_id

        # Create CustomRowWidget instance
        custom_row_widget = CustomRowWidget(
            property_id=property_id, 
            property_key_content=property_key, 
            property_type=property_type, 
            property_value=property_value,  
            types_of_properties=TYPES_OF_PROPERTIES, 
            parent=self,
            row_id = row_id)
        # Store widget in dictionary for easy lookup by ID
        self.dict_row_widgets[row_id] = custom_row_widget
        
        # Connect custom signals from CustomRowWidget to slots in main window
        custom_row_widget.requested_move_up.connect(self.move_row_up)
        custom_row_widget.requested_move_down.connect(self.move_row_down) 
        custom_row_widget.requested_delete.connect(self.delete_row) 
        custom_row_widget.requested_value_changed.connect(lambda: self._save_template()) 
        custom_row_widget.requested_duplicate_no_content.connect(self.duplicate_row_no_content)
        custom_row_widget.requested_duplicate_with_content.connect(self.duplicate_row_with_content)

        
        current_order = self._get_current_order() 
        if position is None:
            # New item
            new_order = current_order + [row_id] 
        else:
            # Insert duplicated row
            # If position is a row_id, convert to index
            # Essentially creates a new ID for this duplicated item
            if position in current_order:
                # Checks if position exists in current order
                # E.g. current order=[0, 2, 1, 3, 4,]; position=2
                # It would be bugged and enter the dupe below 1 instead of 2
                # This is because I don't save specific index for each row/properties
                idx = current_order.index(position)
                insert_at = idx + 1
            else:
                # If position is already an index, use as is
                # This is an error handle -> somehow current_order element is not a number
                insert_at = position + 1 if isinstance(position, int) else len(current_order)
            new_order = current_order[:insert_at] + [row_id] + current_order[insert_at:] 

        # Rebuild entire layout to incorporate new row in its correct position
        self._rebuild_layout_from_order(new_order)
        # new row is added to end of current order, and then layout is rebuilt.
        # This ensures it appears above "Add New" button.


    def _add_new_row_button(self): 
        button = QToolButton()
        button.setText(f"Add New Property")
        button.setMinimumSize(100, 25)
        button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup) # Shows a separate arrow for menu

        options_menu = QMenu(self) 

        for property_type in TYPES_OF_PROPERTIES: 
            property_text = property_type.capitalize().replace('_', ' ')
            options_text = QAction(property_text, self)
            # NOTE: This lambda uses closure to capture current property_type, 
            # Without it, all actions would use the last property_type in the loop.
            # This is because without closure, lambda captures the variable, not its value.
            # i.e. reference to property_type, 
            # not its value at the time of creation. (Hence final value of TYPES_OF_PROPERTIES)
            options_text.triggered.connect(lambda checked, t=property_type: 
                                           self._add_new_row(
                                                property_id=None,
                                                property_key=f"{t.capitalize().replace('_', ' ')}",
                                                property_type=t, 
                                                property_value=f"{t.capitalize().replace('_', ' ')} for {self.current_row_id}"))
            options_menu.addAction(options_text)  

        button.setMenu(options_menu)

        self.add_new_button_widget = button 
        self._rebuild_layout_from_order(self._get_current_order())

    
    def _get_current_order(self) -> list[int]:
        """
        Inspects QGridLayout to determine current visual order
        of CustomRowWidget instances by their row_id.
        This list represents logical order of rows.
        """
        order = []
        # Iterate through all rows in grid layout
        for r in range(self.content_grid.rowCount()):
            # Get item in first column of current row
            item = self.content_grid.itemAtPosition(r, 0)
            if item and item.widget():
                widget = item.widget()
                # If it's a CustomRowWidget, add its row_id to order list
                if isinstance(widget, CustomRowWidget):
                    # order.append(widget.property_id)
                    # Find the row_id for this widget
                    for row_id, w in self.dict_row_widgets.items():
                        if w is widget:
                            order.append(row_id)
                            break
        return order
    
    

    # --- Custom Row Request Handling ---
    
    def update_updown_button_states(self):
        """
        Iterates through all CustomRowWidget instances and enables/disables
        their 'Up' and 'Down' buttons based on their current position in grid.
        """
        current_order_ids = self._get_current_order()
        num_custom_rows = len(current_order_ids)

        for i, row_id in enumerate(current_order_ids):
            widget = self.dict_row_widgets[row_id]
            # Enable 'Up' button if it's not first custom row
            widget.up_button.setEnabled(i > 0) 
            # Enable 'Down' button if it's not last custom row
            widget.down_button.setEnabled(i < num_custom_rows - 1)

    def move_row_up(self, row_id_to_move: int):
        """
        Moves CustomRowWidget with given row_id up one position in grid.
        """
        current_order_ids = self._get_current_order()
        try:
            current_index = current_order_ids.index(row_id_to_move)
            if current_index > 0: # Check if it's not already first item
                # Swap row_ids in order list
                current_order_ids[current_index], current_order_ids[current_index - 1] = \
                    current_order_ids[current_index - 1], current_order_ids[current_index]
                
                # Rebuild layout based on updated order
                self._rebuild_layout_from_order(current_order_ids)
                
            self._save_template()
        except ValueError:
            # This should ideally not happen if row_id_to_move is valid
            print(f"CustomPropertyWidget: Error: Row with ID {row_id_to_move} not found in current order.")
        
        self.update_updown_button_states() # Update button states after move

    def move_row_down(self, row_id_to_move: int):
        """
        Moves CustomRowWidget with given row_id down one position in grid.
        """
        current_order_ids = self._get_current_order()
        try:
            current_index = current_order_ids.index(row_id_to_move)
            if current_index < len(current_order_ids) - 1: # Check if it's not already last item
                # Swap row_ids in order list
                current_order_ids[current_index], current_order_ids[current_index + 1] = \
                    current_order_ids[current_index + 1], current_order_ids[current_index]
                
                # Rebuild layout based on updated order
                self._rebuild_layout_from_order(current_order_ids)
            self._save_template()
        except ValueError: 
            print(f"CustomPropertyWidget: Error: Row with ID {row_id_to_move} not found in current order.")
            
        self.update_updown_button_states() # Update button states after move

    def delete_row(self, row_id_to_delete: int):
        """
        Prompts with Dialog Window, Delete row in row_id when accepted.
        """
        widget_to_delete = self.dict_row_widgets.get(row_id_to_delete)
        if not widget_to_delete:
            print(f"CustomPropertyWidget: Warning: Widget for ID {row_id_to_delete} not found in tracking dictionary.")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{widget_to_delete.property_key_content}'?\n"
            "This action will remove this property in all views.\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No # Default button is No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # User confirmed, proceed with deletion
            # Remove the row_id from logical order list 
            current_order_ids = self._get_current_order()
            try:
                current_order_ids.remove(row_id_to_delete)
            except ValueError:
                print(f"CustomPropertyWidget: Error: Row with ID {row_id_to_delete} not found for deletion after confirmation.")
                return

            self.dict_row_widgets.pop(row_id_to_delete, None)
            widget_to_delete.deleteLater()
            self._rebuild_layout_from_order(current_order_ids)
            self.update_updown_button_states() # Update button states for remaining rows
            # Save to current entry json
            self._save_template()
        else:
            print(f"CustomPropertyWidget: Warning: Widget for ID {row_id_to_delete} not found in tracking dictionary.")

    def duplicate_row_no_content(
            self, 
            row_id: int, 
            property_key: str, 
            property_type: str):
        """
        Duplicates a row without content.
        Creates a new CustomRowWidget with the same properties as the original.
        """
        print(f"CustomPropertyWidget: Duplicating row without content: {row_id} with key '{property_key}' and id '{property_type}'.") 
        self._add_new_row(
            property_id=None,
            property_key=property_key, 
            property_type=property_type, 
            property_value="", 
            position=row_id)


    def duplicate_row_with_content(self, row_id: int, property_key: str, property_type: str, new_value: str):
        """
        Duplicates a row with its content.
        Creates a new CustomRowWidget with the same properties as the original.
        """ 
        print(f"CustomPropertyWidget: Duplicating row: {row_id} with key '{property_key}' and type '{property_type}'") 
        self._add_new_row(
            property_id=None, 
            property_key=property_key, 
            property_type=property_type, 
            property_value=new_value, 
            position=row_id)