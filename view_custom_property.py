# view_custom_property.py
# To customize one's diary property
# Title and date must exist

# TODO: Will be reused to view individual day content

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QToolButton, QLabel, QLineEdit, QPushButton, QDateEdit, 
    QScrollArea, QMenu, QMessageBox,
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QDate

from asset.css_cheatsheet import (
    MAIN_LABEL_LIGHT_QSS, MAIN_LABEL_DARK_QSS,  
)

# --- Custom Row Widget ---
class CustomRowWidget(QWidget):
    """
    A custom widget representing a single row in grid,
    containing Up/Down buttons, a button (property), and a line edit.
    TODO: Line Edit to be edited according to property type.
    TODO: image asset for `Up`, `Down` and `Delete` instead of Unicode and Emoji.
    It emits signals when its Up/Down buttons are clicked.
    """
    move_up_requested = pyqtSignal(int)    # Signal: emitted when 'Up' button is clicked (passes row_id)
    move_down_requested = pyqtSignal(int)  # Signal: emitted when 'Down' button is clicked (passes row_id)
    delete_requested = pyqtSignal(int)    # Signal: emitted when 'Delete' button is clicked (passes row_id)

    def __init__(self, row_id: int, text_content: str, line_edit_value: str = "", parent=None):
        super().__init__(parent)
        self.row_id = row_id # Unique identifier for this specific row widget
        self.text_content = text_content

        # Set up horizontal layout for this row's widgets
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0) 
        self.layout.setSpacing(5)  

        # Create 'Up' button
        self.up_button = QPushButton("▲") # Placeholder for button
        self.up_button.setFixedSize(30, 25) 
        self.up_button.clicked.connect(lambda: self.move_up_requested.emit(self.row_id))

        # Create 'Down' button
        self.down_button = QPushButton("▼") # Placeholder for button
        self.down_button.setFixedSize(30, 25)   
        self.down_button.clicked.connect(lambda: self.move_down_requested.emit(self.row_id))

        # Create 'Text' button
        self.text_button = QPushButton(text_content) 
        self.text_button.setFixedSize(100, 25)
        self.text_button.clicked.connect(lambda: print(f"Text button '{text_content}' in row {self.row_id} clicked!"))

        # Create Line Edit
        self.line_edit = QLineEdit(f"Data for {row_id}")
        self.line_edit.setText(line_edit_value)  

        # Create Delete Button
        self.delete_button = QPushButton("🗑️") # Placeholder for button
        self.delete_button.setFixedSize(30, 25)   
        self.delete_button.clicked.connect(lambda: self.delete_requested.emit(self.row_id))

        # Add widgets to row's horizontal layout
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.text_button)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.delete_button)


# --- Custom Property Widget ---
class CustomPropertyWidget(QWidget):
    """ Actually a view"""
    back_to_main_requested = pyqtSignal()
    settings_saved = pyqtSignal() # Emitted after settings are saved to diary_manager

    def __init__(self, config_manager, diary_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager # For theme 
        self.diary_manager = diary_manager # Store reference to diary manager
        self._setup_ui()
        self._connect_signals()
        self._load_initial_rows_from_config() 

    def _setup_ui(self):

        # Header section for custom property page
        page_header_h_layout = QHBoxLayout() 
        self.main_label = QLabel("Customize Diary Property")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter) 
        self.back_button = QPushButton("Back to Main")
        page_header_h_layout.addWidget(self.main_label, 1)
        page_header_h_layout.addWidget(self.back_button)

        # --- Header grid content ---
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
        
        # --- Dynamic Button - Drop Down menu --- 
        self.content_grid = QGridLayout(self)
        self.content_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_grid.setContentsMargins(10, 10, 10, 10)
        self.content_grid.setSpacing(10)

        # Dictionary to store CustomRowWidget instances, mapped by unique row_id
        self.dict_row_widgets = {}
        self.current_row_id = 0 # Counter for generating unique row_ids
        

        # Special Button that mildly resembles Notion database' property system
        # Reference to "Add New" button widget.
        # Will always be at the very bottom of grid.
        self.add_new_button_widget = None
        self.add_new_row_button()

        # After initial setup, update state of Up/Down buttons
        self.update_button_states()

        # Make Content Grid scrollable
        view_scroll_widget = QWidget()
        view_scroll_widget.setLayout(self.content_grid)
        grid_scroll_area = QScrollArea()
        grid_scroll_area.setWidgetResizable(True)
        grid_scroll_area.setWidget(view_scroll_widget)
        grid_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        grid_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # --- End ---
        page_mainv_layout = QVBoxLayout(self)
        page_mainv_layout.setContentsMargins(15, 15, 15, 15)
        page_mainv_layout.setSpacing(0)
        
        # Header Grid
        # Initialized early to take into consideration of dynamic buttons' shenanigans
        self.header_grid = QGridLayout()
        self.header_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.header_grid.setContentsMargins(0, 0, 0, 0)
        self.header_grid.setSpacing(10)
        
        self.header_grid.addWidget(self.title_label, 0, 0)
        self.header_grid.addWidget(self.title_edit, 0, 1)
        self.header_grid.addWidget(self.date_label, 1, 0)
        self.header_grid.addWidget(self.date_edit, 1, 1)

        # Main Layout filling
        page_mainv_layout.addLayout(page_header_h_layout) 
        page_mainv_layout.addSpacing(10)
        page_mainv_layout.addLayout(self.header_grid)
        page_mainv_layout.addSpacing(10)
        page_mainv_layout.addWidget(grid_scroll_area, 1)
        page_mainv_layout.stretch(1)

    
    def load_into_ui(self):
        """
        Loads current diary property settings into the UI widgets.
        This is called when the widget is displayed.
        """
        self.title_edit.setText(self.diary_manager.get_setting('title', ''))
        self.date_edit.setDate(QDate.fromString(self.diary_manager.get_setting('date', ''), "dd/MM/yyyy"))


    def _connect_signals(self):
        self.back_button.clicked.connect(self._on_back_button_clicked)  

    def _on_back_button_clicked(self):
        self._save_template()
        self.back_to_main_requested.emit()
    
    # --- Load and Save Template Logics ---
    def _save_template(self):
        """
        Gathers data from all dynamic rows and saves it as the JSON template
        using the ConfigManager.
        """
        data_to_save = []
        ordered_ids = self._get_current_order()

        for row_id in ordered_ids:
            widget = self.dict_row_widgets.get(row_id)
            if widget:
                row_data = {
                    "text_button_content": widget.text_button.text(),
                    "line_edit_value": widget.line_edit.text()
                }
                data_to_save.append(row_data)
        
        self.diary_manager.set_setting('dynamic_rows', data_to_save)

        try:
            self.diary_manager.save_config()
            print(f"Template saved successfully to {self.diary_manager.config_file_path}")
        except Exception as e:
            print(f"Error saving template: {e}")
            print(f"Failed to save template to {self.diary_manager.config_file_path}")  

    def _load_initial_rows_from_config(self):
        """
        Loads the dynamic row data (the template) from the config manager
        and populates the grid. Called once on application startup.
        """
        loaded_template_data = self.diary_manager.get_setting('dynamic_rows', [])
        
        self._clear_all_rows()
        
        self.next_row_id = 0 

        if loaded_template_data:
            print(f"Loading {len(loaded_template_data)} dynamic rows (template) from config.")
            for row_data in loaded_template_data:
                text_content = row_data.get("text_button_content", "Loaded Item")
                line_edit_value = row_data.get("line_edit_value", "")
                self.add_row(text_content, line_edit_value)
        else:
            print("No dynamic rows (template) found in config. Starting with an empty template.")
            self._rebuild_layout_from_order([])

        self.update_button_states()

    def _clear_all_rows(self):
        """Helper to clear all DraggableRowWidgets from the grid."""
        current_order_ids = self._get_current_order()
        for row_id in current_order_ids:
            widget = self.dict_row_widgets.pop(row_id, None)
            if widget:
                widget.deleteLater()

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
        
        # Request layout to update itself to reflect changes
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
    def add_new_row_button(self): 
        button = QToolButton()
        button.setText(f"Add New Property")
        button.setMinimumSize(100, 25)
        button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup) # Shows a separate arrow for menu
        
        options_menu = QMenu(self)
        options_text = QAction("Text", self)
        options_text.triggered.connect(lambda: self.add_edit_text())
        options_menu.addAction(options_text)
        
        options_number = QAction("Number", self)
        options_number.triggered.connect(lambda: self.add_edit_number())
        options_menu.addAction(options_number)

        button.setMenu(options_menu)

        self.add_new_button_widget = button 
        self._rebuild_layout_from_order(self._get_current_order())

    def add_row(self, text_content: str, line_edit_value: str = ""):
        """
        Creates a new CustomRowWidget and adds it to grid.
        new row is always added just above 'Add New' button.
        """
        # Generate a unique ID for new row
        row_id = self.current_row_id
        self.current_row_id += 1

        # Create CustomRowWidget instance
        custom_row_widget = CustomRowWidget(row_id, text_content, line_edit_value, self)
        # Store widget in dictionary for easy lookup by ID
        self.dict_row_widgets[row_id] = custom_row_widget
        
        # Connect custom signals from CustomRowWidget to slots in main window
        custom_row_widget.move_up_requested.connect(self.move_row_up)
        custom_row_widget.move_down_requested.connect(self.move_row_down)
        custom_row_widget.delete_requested.connect(self.delete_row)

        # Rebuild entire layout to incorporate new row in its correct position
        self._rebuild_layout_from_order(self._get_current_order() + [row_id])
        # new row is added to end of current order, and then layout is rebuilt.
        # This ensures it appears above "Add New" button.

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
                    order.append(widget.row_id)
        return order

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

        except ValueError:
            # This should ideally not happen if row_id_to_move is valid
            print(f"Error: Row with ID {row_id_to_move} not found in current order.")
        
        self.update_button_states() # Update button states after move

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

        except ValueError: 
            print(f"Error: Row with ID {row_id_to_move} not found in current order.")
            
        self.update_button_states() # Update button states after move

    def delete_row(self, row_id_to_delete: int):
        """
        Prompts with Dialog Window, Delete row in row_id when accepted.
        """
        widget_to_delete = self.dict_row_widgets.get(row_id_to_delete)
        if not widget_to_delete:
            print(f"Warning: Widget for ID {row_id_to_delete} not found in tracking dictionary.")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the row: '{widget_to_delete.text_content}' (ID: {row_id_to_delete})?\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No # Default button is No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # User confirmed, proceed with deletion
            # 1. Remove the row_id from our logical order list
            current_order_ids = self._get_current_order()
            try:
                current_order_ids.remove(row_id_to_delete)
            except ValueError:
                print(f"Error: Row with ID {row_id_to_delete} not found for deletion after confirmation.")
                return

            self.dict_row_widgets.pop(row_id_to_delete, None)
            widget_to_delete.deleteLater()
            self._rebuild_layout_from_order(current_order_ids)
            self.update_button_states() # Update button states for remaining rows
        else:
            print(f"Warning: Widget for ID {row_id_to_delete} not found in tracking dictionary.")

    

    def update_button_states(self):
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

    # --- Fun properties ---
    def add_edit_text(self): 
        print("Custom Property: Add 'text' pressed") 
        self.add_row(f"Text {self.current_row_id}")
        

    def add_edit_number(self):
        print("Custom Property: Add 'number' pressed") 
        self.add_row(f"Number {self.current_row_id}")