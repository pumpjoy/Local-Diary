from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QGridLayout, QPushButton, QLineEdit, QMenu, QToolButton,
    QHBoxLayout, QMessageBox, QVBoxLayout, QFileDialog
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal, QStandardPaths, QDir
import sys
import json
import os 

# --- Configuration Manager Class ---
class DiaryPropertyConfiguration:
    def __init__(self, organization_name="TestOrg", application_name="Local_Diary"):
        """
        Initializes the configuration manager.
        Sets up the path to the config file and loads existing settings or defaults.
        """
        self.organization_name = organization_name
        self.application_name = application_name

        self.config_dir = self._get_config_directory()
        self.config_file_path = os.path.join(self.config_dir, "diary_property.json")
        self.config_data = {}
        
        self._ensure_config_directory_exists()
        self.load_config()

    def _get_config_directory(self):
        """
        Determines the standard, platform-specific directory for application configuration files.
        """
        config_location = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppConfigLocation
        )
        if not config_location:
            config_location = os.path.join(
                QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation),
                f".{self.organization_name}",
                self.application_name
            )
        return config_location

    def _ensure_config_directory_exists(self):
        """
        Creates the configuration directory if it doesn't already exist.
        """
        if not QDir().mkpath(self.config_dir):
            print(f"Warning: Could not create config directory: {self.config_dir}")

    def load_config(self):
        """
        Loads configuration data from the config file.
        If file doesn't exist or is corrupted, it initializes with default settings.
        """
        if os.path.exists(self.config_file_path):
            try:
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                print(f"Configuration loaded from: {self.config_file_path}")
            except json.JSONDecodeError as e:
                print(f"Error loading config file (JSON decode error): {e}")
                print("Initializing with default settings.")
                self.config_data = self._get_default_config()
            except Exception as e:
                print(f"Error loading config file: {e}")
                print("Initializing with default settings.")
                self.config_data = self._get_default_config()
        else:
            print(f"Config file not found: {self.config_file_path}. Initializing with default settings.")
            self.config_data = self._get_default_config()

    def save_config(self):
        """
        Saves the current in-memory configuration data to the config file.
        """
        try:
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
            print(f"Configuration saved to: {self.config_file_path}")
            return True
        except Exception as e:
            print(f"Error saving config file: {e}")
            return False

    def get_setting(self, key, default_value=None):
        """
        Retrieves a setting by key.
        Supports nested keys using dot notation (e.g., 'section.item').
        Returns a default_value if the key is not found.
        """
        parts = key.split('.')
        current = self.config_data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default_value
        return current

    def set_setting(self, key, value):
        """
        Sets a setting's value, supporting nested keys using dot notation.
        Creates nested dictionaries if they don't exist.
        """
        parts = key.split('.')
        current = self.config_data
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                current[part] = value
            else:
                if part not in current or not isinstance(current[part], dict):
                    current[part] = {}
                current = current[part]

    def _get_default_config(self):
        """
        Defines the default structure and values for the application's configuration.
        """ 
        return {
            "title": "Default Diary Title",
            "date": "2025-07-31",
            "description": "Default descriptions for the diary entries.",
            "dynamic_rows": []
        }

# --- Custom Draggable Row Widget ---
class DraggableRowWidget(QWidget):
    """
    A custom widget representing a single row in the grid.
    Its action menu and type-selection menu are built dynamically from a list of available types.
    """
    move_up_requested = pyqtSignal(int)
    move_down_requested = pyqtSignal(int)
    delete_requested = pyqtSignal(int)
    type_changed = pyqtSignal(int, str)

    def __init__(self, row_id: int, text_content: str, line_edit_value: str = "", 
                 row_type: str = "Type A", available_types: list[str] = None, parent=None):
        super().__init__(parent)
        self.row_id = row_id
        self.text_content = text_content
        self.row_type = row_type
        self.available_types = available_types if available_types is not None else ["Type A", "Type B"]

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        self.up_button = QPushButton("▲")
        self.up_button.setFixedSize(25, 25)
        self.up_button.clicked.connect(lambda: self.move_up_requested.emit(self.row_id))

        self.down_button = QPushButton("▼")
        self.down_button.setFixedSize(25, 25)
        self.down_button.clicked.connect(lambda: self.move_down_requested.emit(self.row_id))

        # Dynamically create the type selection menu
        self.type_menu_button = QToolButton()
        self.type_menu_button.setText(f"{self.row_type}")
        self.type_menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        type_menu = QMenu(self)
        self.type_label_action = QAction(f"Current Type: {self.row_type}", self)
        self.type_label_action.setDisabled(True)
        type_menu.addAction(self.type_label_action)
        type_menu.addSeparator()

        # Iterate over the dynamic list of types to create the menu options
        for type_option in self.available_types:
            action = type_menu.addAction(type_option)
            action.triggered.connect(lambda _, t=type_option: self._set_row_type(t))
        self.type_menu_button.setMenu(type_menu)

        # A button for the type-specific actions
        self.action_menu_button = QToolButton()
        self.action_menu_button.setText("Actions")
        self.action_menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.text_button = QPushButton(text_content)
        self.line_edit = QLineEdit()
        self.line_edit.setText(line_edit_value)

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(25, 25)
        self.delete_button.clicked.connect(lambda: self.delete_requested.emit(self.row_id))

        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.type_menu_button)
        self.layout.addWidget(self.action_menu_button)
        self.layout.addWidget(self.text_button)
        self.layout.addWidget(self.line_edit)
        self.layout.addStretch(1)
        self.layout.addWidget(self.delete_button)
        
        self._update_action_menu()

    def _set_row_type(self, new_type: str):
        """
        Updates the row's type and all associated UI elements.
        """
        if self.row_type != new_type:
            self.row_type = new_type
            self.type_menu_button.setText(self.row_type)
            self.type_label_action.setText(f"Current Type: {self.row_type}")
            self._update_action_menu() 
            self.type_changed.emit(self.row_id, self.row_type)
    
    def _update_action_menu(self):
        """
        Dynamically creates and sets the action menu based on the current row type.
        """
        if self.row_type == "Type A":
            menu = self._create_menu_for_type_A()
        elif self.row_type == "Type B":
            menu = self._create_menu_for_type_B()
        else:
            # Handle unknown or new types gracefully
            menu = QMenu(self) 
            menu.addAction(f"No actions for type: {self.row_type}")
        
        self.action_menu_button.setMenu(menu)

    def _create_menu_for_type_A(self):
        """Creates a QMenu with actions specific to Type A."""
        menu = QMenu(self)
        menu.addAction("Action 1 (Type A)").triggered.connect(lambda: print(f"Row {self.row_id}: Action 1 for Type A triggered"))
        menu.addAction("Action 2 (Type A)").triggered.connect(lambda: print(f"Row {self.row_id}: Action 2 for Type A triggered"))
        menu.addSeparator()
        menu.addAction("Common Action").triggered.connect(lambda: print(f"Row {self.row_id}: Common Action triggered"))
        return menu
    
    def _create_menu_for_type_B(self):
        """Creates a QMenu with actions specific to Type B."""
        menu = QMenu(self)
        menu.addAction("Special Action (Type B)").triggered.connect(lambda: print(f"Row {self.row_id}: Special Action for Type B triggered"))
        menu.addAction("Another Action (Type B)").triggered.connect(lambda: print(f"Row {self.row_id}: Another Action for Type B triggered"))
        menu.addSeparator()
        menu.addAction("Common Action").triggered.connect(lambda: print(f"Row {self.row_id}: Common Action triggered"))
        return menu


# --- Main Window / Top-level Widget ---
class DynamicGridExample(QWidget):
    """
    A PyQt6 application for creating and editing a JSON template.
    This application's list of row types is now dynamically configured.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Template Editor (Dynamic Rows)")
        self.setGeometry(100, 100, 900, 500)

        self.config_manager = DiaryPropertyConfiguration()
        
        # This is the master list of available types.
        # This can be loaded from a configuration file for true dynamism.
        self.available_types = ["Type A", "Type B", "Type C"]

        self.main_layout = QVBoxLayout(self)

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(10)

        self.control_buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Template")
        self.save_button.clicked.connect(self.save_configuration)
        self.load_button = QPushButton("Load Template")
        self.load_button.clicked.connect(self.load_configuration)

        self.control_buttons_layout.addStretch(1)
        self.control_buttons_layout.addWidget(self.save_button)
        self.control_buttons_layout.addWidget(self.load_button)
        self.control_buttons_layout.addStretch(1)

        self.main_layout.addLayout(self.control_buttons_layout)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addStretch(1)

        self.row_widgets_by_id = {} 
        self.next_row_id = 0      

        self.add_new_button_widget = None 
        self._create_add_new_button()

        self._load_initial_rows_from_config()

        self.update_button_states()

    def _create_add_new_button(self):
        """
        Creates the 'Add New' button with a dynamic menu based on available types.
        """
        add_button = QToolButton()
        add_button.setText("Add New")
        add_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup) 

        menu = QMenu(self) 
        for row_type in self.available_types:
            action = QAction(f"Add {row_type}", self)
            action.triggered.connect(
                lambda _, t=row_type: self.add_draggable_row(f"New Item {self.next_row_id}", "", t)
            )
            menu.addAction(action)
        add_button.setMenu(menu)
        self.add_new_button_widget = add_button

    def _load_initial_rows_from_config(self):
        """
        Loads the dynamic row data (the template) from the config manager
        and populates the grid.
        """
        loaded_template_data = self.config_manager.get_setting('dynamic_rows', [])
        
        self._clear_all_draggable_rows()
        self.next_row_id = 0 

        if loaded_template_data:
            print(f"Loading {len(loaded_template_data)} dynamic rows (template) from config.")
            for row_data in loaded_template_data:
                text_content = row_data.get("text_button_content", "Loaded Item")
                line_edit_value = row_data.get("line_edit_value", "")
                row_type = row_data.get("type", self.available_types[0]) # Use the first available type as a fallback
                self.add_draggable_row(text_content, line_edit_value, row_type)
        else:
            print("No dynamic rows (template) found in config. Starting with an empty template.")
            self._rebuild_layout_from_order([])

        self.update_button_states()

    def add_draggable_row(self, text_content: str, line_edit_value: str = "", row_type: str = "Type A"):
        """
        Creates a new DraggableRowWidget and adds it to the grid.
        Passes the available types to the new row.
        """
        row_id = self.next_row_id
        self.next_row_id += 1

        draggable_widget = DraggableRowWidget(row_id, text_content, line_edit_value, row_type, self.available_types, self)
        self.row_widgets_by_id[row_id] = draggable_widget
        
        draggable_widget.move_up_requested.connect(self.move_row_up)
        draggable_widget.move_down_requested.connect(self.move_row_down)
        draggable_widget.delete_requested.connect(self.delete_row)

        self._rebuild_layout_from_order(self._get_current_draggable_order() + [row_id])


    def _get_current_draggable_order(self) -> list[int]:
        """
        Inspects the QGridLayout to determine the current visual order
        of DraggableRowWidget instances by their row_id.
        """
        order = []
        for r in range(self.grid_layout.rowCount()):
            item = self.grid_layout.itemAtPosition(r, 0)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, DraggableRowWidget):
                    order.append(widget.row_id)
        return order


    def move_row_up(self, row_id_to_move: int):
        """Moves the DraggableRowWidget with the given row_id up one position."""
        current_order_ids = self._get_current_draggable_order()
        try:
            current_index = current_order_ids.index(row_id_to_move)
            if current_index > 0:
                current_order_ids[current_index], current_order_ids[current_index - 1] = \
                    current_order_ids[current_index - 1], current_order_ids[current_index]
                self._rebuild_layout_from_order(current_order_ids)
        except ValueError:
            print(f"Error: Row with ID {row_id_to_move} not found in current order.")
        self.update_button_states()


    def move_row_down(self, row_id_to_move: int):
        """Moves the DraggableRowWidget with the given row_id down one position."""
        current_order_ids = self._get_current_draggable_order()
        try:
            current_index = current_order_ids.index(row_id_to_move)
            if current_index < len(current_order_ids) - 1:
                current_order_ids[current_index], current_order_ids[current_index + 1] = \
                    current_order_ids[current_index + 1], current_order_ids[current_index]
                self._rebuild_layout_from_order(current_order_ids)
        except ValueError:
            print(f"Error: Row with ID {row_id_to_move} not found in current order.")
        self.update_button_states()

    def delete_row(self, row_id_to_delete: int):
        """Deletes the DraggableRowWidget with the given row_id from the grid, after confirming."""
        widget_to_delete = self.row_widgets_by_id.get(row_id_to_delete)
        if not widget_to_delete:
            print(f"Warning: Widget for ID {row_id_to_delete} not found in tracking dictionary.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the row: '{widget_to_delete.text_content}' (ID: {row_id_to_delete})?\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            current_order_ids = self._get_current_draggable_order()
            try:
                current_order_ids.remove(row_id_to_delete)
            except ValueError:
                print(f"Error: Row with ID {row_id_to_delete} not found for deletion after confirmation.")
                return

            self.row_widgets_by_id.pop(row_id_to_delete, None)
            
            widget_to_delete.deleteLater()
            
            self._rebuild_layout_from_order(current_order_ids)
            self.update_button_states()
        else:
            print(f"Deletion of row ID {row_id_to_delete} cancelled by user.")


    def _rebuild_layout_from_order(self, new_order_ids: list[int]):
        """
        Clears the entire QGridLayout and then re-adds all active widgets
        in the specified new order.
        """
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None) 

        current_grid_row = 0
        for row_id in new_order_ids:
            if row_id in self.row_widgets_by_id:
                widget = self.row_widgets_by_id[row_id]
                self.grid_layout.addWidget(widget, current_grid_row, 0, 1, self.grid_layout.columnCount())
                current_grid_row += 1
        
        if self.add_new_button_widget:
            self.grid_layout.addWidget(self.add_new_button_widget, current_grid_row, 0, 1, self.grid_layout.columnCount())
        
        self.grid_layout.update()


    def update_button_states(self):
        """Enables/disables 'Up' and 'Down' buttons based on their current position."""
        current_order_ids = self._get_current_draggable_order()
        num_draggable_rows = len(current_order_ids)

        for i, row_id in enumerate(current_order_ids):
            if row_id in self.row_widgets_by_id:
                widget = self.row_widgets_by_id[row_id]
                widget.up_button.setEnabled(i > 0) 
                widget.down_button.setEnabled(i < num_draggable_rows - 1)

    def save_configuration(self):
        """
        Gathers data from all dynamic rows and saves it as the JSON template
        using the ConfigManager.
        """
        data_to_save = []
        ordered_ids = self._get_current_draggable_order()

        for row_id in ordered_ids:
            widget = self.row_widgets_by_id.get(row_id)
            if widget:
                row_data = {
                    "text_button_content": widget.text_button.text(),
                    "line_edit_value": widget.line_edit.text(),
                    "type": widget.row_type
                }
                data_to_save.append(row_data)
        
        self.config_manager.set_setting('dynamic_rows', data_to_save)

        if self.config_manager.save_config():
            QMessageBox.information(self, "Save Successful", 
                                    f"Template saved to:\n{self.config_manager.config_file_path}")
        else:
            QMessageBox.critical(self, "Save Failed", "Could not save template.")


    def load_configuration(self):
        """
        Loads the JSON template from the configuration file and reconstructs the dynamic rows.
        This discards current unsaved changes to the template.
        """
        reply = QMessageBox.question(
            self,
            "Confirm Load Template",
            "Loading a new template will clear all existing rows and discard unsaved changes.\n"
            "Do you want to continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.config_manager.load_config()
            loaded_template_data = self.config_manager.get_setting('dynamic_rows', [])

            self._clear_all_draggable_rows()
            self.next_row_id = 0

            if loaded_template_data:
                for row_data in loaded_template_data:
                    text_content = row_data.get("text_button_content", "Loaded Item")
                    line_edit_value = row_data.get("line_edit_value", "")
                    # Use the first available type as a fallback if the loaded type is unknown
                    row_type = row_data.get("type", self.available_types[0])
                    self.add_draggable_row(text_content, line_edit_value, row_type)
            else:
                self._rebuild_layout_from_order([])
            
            self.update_button_states()
            QMessageBox.information(self, "Load Successful", 
                                    f"Template loaded from:\n{self.config_manager.config_file_path}")
        else:
            print("Template load operation cancelled by user.")

    def _clear_all_draggable_rows(self):
        """Helper to clear all DraggableRowWidgets from the grid."""
        current_order_ids = self._get_current_draggable_order()
        for row_id in current_order_ids:
            widget = self.row_widgets_by_id.pop(row_id, None)
            if widget:
                widget.deleteLater()


# --- Application Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = DynamicGridExample()
    window.show() 
    sys.exit(app.exec())