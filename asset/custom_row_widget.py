from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QWidgetAction, QStackedWidget,
    QToolButton, QLabel, QLineEdit, QPushButton, QDateEdit, 
    QScrollArea, QMenu, QMessageBox,
)
from PyQt6.QtGui import QAction, QIntValidator
from PyQt6.QtCore import Qt, QDate

from asset.css_cheatsheet import TYPES_OF_PROPERTIES  

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
    value_changed_requested = pyqtSignal(int, str, str, str)  # Signal: emitted when value is changed (passes row_id and 3 new values)

    def __init__(self, row_id: int, 
                 property_key_content: str, property_type: str, property_value_content: str = "",
                 types_of_properties: list[str]=None,
                 parent=None):
        super().__init__(parent)

        self.row_id = row_id
        self.property_key_content = property_key_content
        self.property_type = property_type
        self.property_value_content = property_value_content
        self.property_value = self.property_value_content # TODO: TEMPORARY
        print(f"Creating CustomRowWidget for row {self.row_id} with property type '{self.property_type}' and value '{self.property_value_content}'")

        self.types_of_properties = types_of_properties
        
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
        self.text_line_edit.setText(self.property_value_content)
        self.text_line_edit.textChanged.connect(self._handle_text_line_changed)
        self.content_stack.addWidget(self.text_line_edit)

        # Widget for Select, Multi Select:
        self.select_bt = QPushButton("Click Me (Select)")
        self.select_bt.clicked.connect(lambda: print("Select / Multiselect clicked."))
        self.content_stack.addWidget(self.select_bt)

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

    # --- Generate full menu for property_key ---
    def _generate_menu_types(self):
        """
        Generates a menu for changing property type.
        """
        menu_change_type = QMenu(self)
        for property_type in TYPES_OF_PROPERTIES: 
            property_text = property_type.capitalize().replace('_', ' ')
            options_text = QAction(property_text, self) 
            options_text.triggered.connect(lambda _, t=property_type: self._set_row_type(new_type=t)) 
            menu_change_type.addAction(options_text) 
        
        menu_change_type.setTitle("Change Type")
        menu_change_type.setToolTip("Change Property Type")

        return menu_change_type
    

    # --- Functions for Menu ---
    ### General
    def _create_line_edit_name(self):
        """Creates a line edit to edit property_key value"""
        # BUG: doesn't react to double_click selectAll() 
        # Maybe turn this whole thing into a Dialog
        name_line_edit = QLineEdit()
        name_line_edit.setText(self.property_key.text())
        name_line_edit.returnPressed.connect(
            lambda: self._rename_property_key(new_key=self.name_line_edit.text()))
        return name_line_edit
    
    def _rename_property_key(self, new_key):
        """
        Renames the property key.
        """
        self.property_key.setText(new_key)
        self.value_changed_requested.emit(
            self.row_id, self.property_key.text(), self.property_type, self.property_value)
    
    ### Text
    def _create_menu_for_text(self):
        """
        Creates a menu for text property type.
        """
        menu = QMenu(self)
        
        ### Line edit to edit property name
        self.name_line_edit = self._create_line_edit_name()
        option_key_edit = QWidgetAction(menu) 
        option_key_edit.setDefaultWidget(self.name_line_edit)
        menu.addAction(option_key_edit)
        
        ### Property Change
        # Visual indicator of what this property is
        property_label = QAction(f"Type: {self.property_type.capitalize().replace('_', ' ')}", self) 
        property_label.setDisabled(True)
        menu.addAction(property_label)

        # Menu for Property Type Change
        menu_change_type = self._generate_menu_types()
        menu_change_type.setTitle("Edit Property Type")
        menu_change_type.setToolTip("Edit Property Type")
        menu.addMenu(menu_change_type)
 
        menu.addSeparator() 

        ### Other options
        options_visibility = QAction("Property Visibility", self)
        options_visibility.triggered.connect(lambda: print(f"Property Visibility in row {self.row_id} clicked!"))
        menu.addAction(options_visibility)
        
        options_duplicate = QAction("Duplicate Property", self)
        options_duplicate.triggered.connect(lambda: print(f"Duplicate Property in row {self.row_id} clicked!"))
        menu.addAction(options_duplicate)
        
        options_delete = QAction("Delete Property", self)
        options_delete.triggered.connect(lambda: self.delete_requested.emit(self.row_id))
        menu.addAction(options_delete)

        return menu 
    
    ### Number
    def _create_menu_for_number(self):
        """
        Creates a menu for number property type.
        """
        menu = QMenu(self)

        self.name_line_edit = self._create_line_edit_name()
        option_key_edit = QWidgetAction(menu) 
        option_key_edit.setDefaultWidget(self.name_line_edit)
        menu.addAction(option_key_edit)

        menu_change_type = self._generate_menu_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Number Property", self)
        options_text.triggered.connect(lambda: print(f"Number Property in row {self.row_id} clicked!"))
        menu.addAction(options_text) 

        return menu 
    
    ### Select
    def _create_menu_for_select(self):
        """
        Creates a menu for select property type.
        """
        menu = QMenu(self)

        self.name_line_edit = self._create_line_edit_name()
        option_key_edit = QWidgetAction(menu) 
        option_key_edit.setDefaultWidget(self.name_line_edit)
        menu.addAction(option_key_edit)


        menu_change_type = self._generate_menu_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Select Property", self)
        options_text.triggered.connect(lambda: print(f"Number Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 
    
    ### Multi Select
    def _create_menu_for_multi_select(self):
        """
        Creates a menu for multi select property type.
        """
        menu = QMenu(self)

        self.name_line_edit = self._create_line_edit_name()
        option_key_edit = QWidgetAction(menu) 
        option_key_edit.setDefaultWidget(self.name_line_edit)
        menu.addAction(option_key_edit)

        menu_change_type = self._generate_menu_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Multi Select Property", self)
        options_text.triggered.connect(lambda: print(f"Multi Select Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 
    
    ### Checkbox
    def _create_menu_for_checkbox(self):
        """
        Creates a menu for checkbox property type.
        """
        menu = QMenu(self)

        self.name_line_edit = self._create_line_edit_name()
        option_key_edit = QWidgetAction(menu) 
        option_key_edit.setDefaultWidget(self.name_line_edit)
        menu.addAction(option_key_edit)

        menu_change_type = self._generate_menu_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Checkbox Property", self)
        options_text.triggered.connect(lambda: print(f"Checkbox Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 
     
    # --- Functions for main widgets --- 
    ### Type: Text, Number
    def _handle_text_line_changed(self, text):
        """Updates the self.text_line_edit"""
        self.property_value_content = text

    # --- Functions for handling updates at changes ---
    def _set_row_type(self, new_type: str):
        """
        Updates the row's type and all associated UI elements.
        Switches the visible widget in the self.content_stack based on the row's type.
        """
        if self.property_type != new_type:
            self.property_type = new_type
            text = self.property_type.capitalize().replace('_', ' ')
            self.type_label_action.setText(text)
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
        elif self.property_type == "checkbox":
            menu2 = self._create_menu_for_checkbox()
        else:
            menu2 = QMenu(self)
        
        self.property_key.setMenu(menu2)
        
        self.value_changed_requested.emit(
            self.row_id, self.property_key.text(), self.property_type, self.property_value)

    def _update_widgets(self):
        if self.property_type == "text":
            print("text")
            self.text_line_edit.setValidator(None)
            self.content_stack.setCurrentWidget(self.text_line_edit)
        elif self.property_type == "number":
            print("number")
            int_validator = QIntValidator()
            self.text_line_edit.setValidator(int_validator)
            self.content_stack.setCurrentWidget(self.text_line_edit)
        elif self.property_type == "select":
            print("select")
            self.content_stack.setCurrentWidget(self.select_bt)
        elif self.property_type == "multi select":
            print("multi select")
            self.content_stack.setCurrentWidget(self.select_bt)
        elif self.property_type == "checkbox":
            print("checkbox")
            self.content_stack.setCurrentWidget(self.checkbox_bt)
