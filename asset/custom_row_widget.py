from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QHBoxLayout,
    QWidget, QWidgetAction, QStackedWidget,
    QToolButton,  QLineEdit, QPushButton, 
    QMenu, 
)
from PyQt6.QtGui import QAction, QIntValidator 

from asset.css_cheatsheet import TYPES_OF_PROPERTIES  
from asset.menu_edit_property import MenuEditProperty

# --- Custom Row Widget ---
class CustomRowWidget(QWidget):
    """
    A custom widget representing a single row in grid,
    containing Up/Down buttons, a button (property), and a line edit. 
    TODO: image asset for `Up`, `Down` and `Delete` instead of Unicode and Emoji.
    It emits signals when its Up/Down buttons are clicked.
    """
    requested_move_up = pyqtSignal(int)    # Signal: emitted when 'Up' button is clicked (passes property_id)
    requested_move_down = pyqtSignal(int)  # Signal: emitted when 'Down' button is clicked (passes property_id)
    requested_delete = pyqtSignal(int)    # Signal: emitted when 'Delete' button is clicked (passes property_id)
    requested_value_changed = pyqtSignal(int, str, str, str)  # Signal: emitted when value is changed (passes property_id and 3 new values)
    requested_duplicate_no_content =  pyqtSignal(int, str, str) # Signal: duplicate row without content
    requested_duplicate_with_content =  pyqtSignal(int, str, str, str) # Signal: duplicate row with content


    def __init__(self, property_id: int,  
                 property_key_content: str, 
                 property_type: str, 
                 property_value: str = "",
                 types_of_properties: list[str]=None,
                 parent=None,
                 row_id: int = None):
        super().__init__(parent)

        self.property_id = property_id # Unique identifier
        self.row_id = row_id # Positional
        self.property_key_content = property_key_content
        self.property_type = property_type 
        self.property_value = property_value

        self.types_of_properties = types_of_properties
        
        # Set up horizontal layout for this row's widgets
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0) 
        self.layout.setSpacing(5)

        # Create 'Up' button
        self.up_button = QPushButton("▲") # Placeholder for button
        self.up_button.setFixedSize(30, 25) 
        self.up_button.clicked.connect(lambda: self.requested_move_up.emit(self.row_id))

        # Create 'Down' button
        self.down_button = QPushButton("▼") # Placeholder for button
        self.down_button.setFixedSize(30, 25)   
        self.down_button.clicked.connect(lambda: self.requested_move_down.emit(self.row_id))

        # Create Property Key Tool button
        self.property_key = QToolButton()
        self.property_key.setFixedSize(100, 25)
        self.property_key.setText(property_key_content) 
        self.property_key.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
         
        self.property_key_menu = QMenu(self)
        # Type Label 
        self.type_label_action = QAction(f"Type: {self.property_type.capitalize().replace('_', ' ')}", self)
        self.type_label_action.setDisabled(True)
        self.property_key_menu.addAction(self.type_label_action)

        # Menu 1: Edit Property
        self.menu1 = QMenu(self) # Init empty
        self.property_key.setMenu(self.menu1)  

        # --- Create Specific Widgets --- 
        self.content_stack = QStackedWidget(self) 
        self.content_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Widget for Text, Number:
        self.text_line_edit = QLineEdit()
        # self.text_line_edit.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self.text_line_edit.setFixedHeight(10)
        self.text_line_edit.setText(self.property_value)
        self.text_line_edit.textChanged.connect(self._handle_text_line_changed)
        self.content_stack.addWidget(self.text_line_edit)

        # Widget for Select:
        self.select_bt = QPushButton("Click Me (Select)")
        self.select_bt.clicked.connect(lambda: print("Select clicked"))
        self.content_stack.addWidget(self.select_bt)

        # Widget for Multi Select:
        self.multi_select_bt = QPushButton("Click Me (Multi Select)")
        self.multi_select_bt.clicked.connect(lambda: print("Multi Select clicked."))
        self.content_stack.addWidget(self.multi_select_bt)

        # Widget for Status:
        self.status_bt = QPushButton("Click Me (Status)")
        self.status_bt.clicked.connect(lambda: print("Status clicked."))
        self.content_stack.addWidget(self.status_bt)

        # Widget for Checkbox:
        self.checkbox_bt = QPushButton("Click Me (Checkbox)")
        self.checkbox_bt.clicked.connect(lambda: print("Checkbox clicked."))
        self.content_stack.addWidget(self.checkbox_bt)

        
        # Add widgets to row's horizontal layout
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.property_key)
        self.layout.addWidget(self.content_stack) 

        # Set the initial state
        self._update_menu()
        self._update_widgets()


    # --- Functions for Menu ---


    def _rename_property_key(self, new_key):
        """
        Renames the property key.
        """
        self.property_key.setText(new_key)
        self.requested_value_changed.emit(
            self.property_id, self.property_key.text(), self.property_type, self.property_value)
 
    def _create_properties_common_menu_options(self):
        """
        Creates 
        Label for Showing property_type
        Options of Visibility, Duplicate and Delete
        """ 
        # Visual indicator of what this property is
        property_label = QAction(f"Type: {self.property_type.capitalize().replace('_', ' ')}", self) 
        property_label.setDisabled(True)
        
        ### Other options
        options_visibility = QAction("Property Visibility", self)
        options_visibility.triggered.connect(lambda: print(f"Property Visibility in row {self.property_id} clicked!"))

        options_duplicate_no_content = QAction("Duplicate without Content Property", self)
        options_duplicate_no_content.triggered.connect(lambda: self.requested_duplicate_no_content.emit(
            self.row_id, self.property_key.text(), self.property_type))
        
        options_duplicate_with_content = QAction("Duplicate with Content Property", self)
        options_duplicate_with_content.triggered.connect(lambda: self.requested_duplicate_with_content.emit(
            self.row_id, self.property_key.text(), self.property_type, self.property_value))
        
        options_delete = QAction("Delete Property", self)
        options_delete.triggered.connect(lambda: self.requested_delete.emit(self.row_id))

        return property_label, options_visibility, options_duplicate_no_content, options_duplicate_with_content, options_delete


    # --- Actual Properties ---
    ### Text
    def _create_menu_for_text(self):
        """
        Creates a menu for text property type.
        """
        menu = QMenu(self)
        property_label, \
            options_visibility, options_duplicate_no_content, options_duplicate_with_content, options_delete = \
            self._create_properties_common_menu_options()
         
        ### Property Change
        # Label to see property type
        menu.addAction(property_label) 
        
        # Special: Menu for Text
        # New menu for text
        # menu_special = 1
        menu_special = MenuEditProperty(self.property_id, self.property_key.text(), self.property_type, self.property_value)
        menu_special._setup_edit_text_ui() 
        menu_special.requested_menu_key_change.connect(self._rename_property_key)
        menu.addMenu(menu_special)

        menu.addSeparator() 

        ### Other options
        menu.addAction(options_visibility)
        menu.addAction(options_duplicate_no_content)
        menu.addAction(options_duplicate_with_content)
        menu.addAction(options_delete)

        return menu 
    
    ### Number
    def _create_menu_for_number(self):
        """
        Creates a menu for number property type.
        """
        menu = QMenu(self)
        property_label, \
            options_visibility, options_duplicate_no_content, options_duplicate_with_content, options_delete = \
            self._create_properties_common_menu_options()
         
        ### Property Change
        # Label to see property type
        menu.addAction(property_label) 
        
        # Special: Menu for Number
        # New menu for number
        # menu_special = 1

        menu.addSeparator() 

        ### Other options
        menu.addAction(options_visibility)
        menu.addAction(options_duplicate_no_content)
        menu.addAction(options_duplicate_with_content)
        menu.addAction(options_delete)

        return menu 
    
    ### Select
    def _create_menu_for_select(self):
        """
        Creates a menu for select property type.
        """
        menu = QMenu(self)
        property_label, \
            options_visibility, options_duplicate_no_content, options_duplicate_with_content, options_delete = \
            self._create_properties_common_menu_options()
         
        ### Property Change
        # Label to see property type
        menu.addAction(property_label) 
        
        # Special: Menu for Select
        # New menu for select
        # menu_special = 1

        menu.addSeparator() 

        ### Other options
        menu.addAction(options_visibility)
        menu.addAction(options_duplicate_no_content)
        menu.addAction(options_duplicate_with_content)
        menu.addAction(options_delete)

        return menu 
    
    ### Multi Select
    def _create_menu_for_multi_select(self):
        """
        Creates a menu for multi select property type.
        """
        menu = QMenu(self)
        property_label, \
            options_visibility, options_duplicate_no_content, options_duplicate_with_content, options_delete = \
            self._create_properties_common_menu_options()
         
        ### Property Change
        # Label to see property type
        menu.addAction(property_label) 
        
        # Special: Menu for Multi Select
        # New menu for multi select
        # menu_special = 1

        menu.addSeparator() 

        ### Other options
        menu.addAction(options_visibility)
        menu.addAction(options_duplicate_no_content)
        menu.addAction(options_duplicate_with_content)
        menu.addAction(options_delete)

        return menu 
    
    ### Status
    def _create_menu_for_status(self):
        """
        Creates a menu for status property type.
        """
        menu = QMenu(self)
        property_label, \
            options_visibility, options_duplicate_no_content, options_duplicate_with_content, options_delete = \
            self._create_properties_common_menu_options()
         
        ### Property Change
        # Label to see property type
        menu.addAction(property_label) 
        
        # Special: Menu for Status
        # New menu for status
        # menu_special = 1

        menu.addSeparator() 

        ### Other options
        menu.addAction(options_visibility)
        menu.addAction(options_duplicate_no_content)
        menu.addAction(options_duplicate_with_content)
        menu.addAction(options_delete)

        return menu 

    ### Checkbox
    def _create_menu_for_checkbox(self):
        """
        Creates a menu for checkbox property type.
        """
        menu = QMenu(self)
        property_label, \
            options_visibility, options_duplicate_no_content, options_duplicate_with_content, options_delete = \
            self._create_properties_common_menu_options()
         
        ### Property Change
        # Label to see property type
        menu.addAction(property_label) 
        
        # Special: Menu for Checkbox
        # New menu for checkbox
        # menu_special = 1

        menu.addSeparator() 

        ### Other options
        menu.addAction(options_visibility)
        menu.addAction(options_duplicate_no_content)
        menu.addAction(options_duplicate_with_content)
        menu.addAction(options_delete)

        return menu 
     
    # --- Functions for main widgets --- 
    ### Type: Text, Number
    def _handle_text_line_changed(self, text):
        """Updates the self.text_line_edit"""
        self.property_value = text

    # --- Functions for handling updates at changes ---
    def _update_row_type(self, new_type: str):
        """
        Updates the row's type and all associated UI elements.
        Switches the visible widget in the self.content_stack based on the row's type.
        """
        if self.property_type != new_type:
            old = self.property_type.capitalize().replace('_', ' ')
            print(f"old = {old} | property_key = {self.property_key.text() }")

            self.property_type = new_type
            text = self.property_type.capitalize().replace('_', ' ')
            self.type_label_action.setText(text)
        
            # Checks if Property Title is changed, if not, change it 
            if self.property_key.text() == old:
                self.property_key.setText(text)
            
            self._update_menu()
            self._update_widgets() 

    def _update_menu(self):
        """
        Updates the menu of property_key button
        """
        if self.property_key.menu() is not None:
            self.property_key.menu().clear()

        if self.property_type == "text":
            menu2 = self._create_menu_for_text()
        elif self.property_type == "number":
            menu2 = self._create_menu_for_number()
        elif self.property_type == "select":
            menu2 = self._create_menu_for_select()
        elif self.property_type == "multi_select":
            menu2 = self._create_menu_for_multi_select()
        elif self.property_type == "status":
            menu2 = self._create_menu_for_status()
        elif self.property_type == "checkbox":
            menu2 = self._create_menu_for_checkbox()
        else:
            menu2 = QMenu(self)
        
        self.property_key.setMenu(menu2)
        
        self.requested_value_changed.emit(
            self.property_id, self.property_key.text(), self.property_type, self.property_value)

    def _update_widgets(self):
        if self.property_type == "text":
            self.text_line_edit.setValidator(None)
            self.content_stack.setCurrentWidget(self.text_line_edit)
        elif self.property_type == "number":
            int_validator = QIntValidator()
            self.text_line_edit.setValidator(int_validator)
            self.content_stack.setCurrentWidget(self.text_line_edit)
        elif self.property_type == "select":
            self.content_stack.setCurrentWidget(self.select_bt)
        elif self.property_type == "multi_select":
            self.content_stack.setCurrentWidget(self.multi_select_bt)
        elif self.property_type == "status":
            self.content_stack.setCurrentWidget(self.status_bt)
        elif self.property_type == "checkbox":
            self.content_stack.setCurrentWidget(self.checkbox_bt)
