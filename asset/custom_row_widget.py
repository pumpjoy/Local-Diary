from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QToolButton, QLabel, QLineEdit, QPushButton, QDateEdit, 
    QScrollArea, QMenu, QMessageBox,
)
from PyQt6.QtGui import QAction
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

    def __init__(self, row_id: int, property_key_content: str, property_type: str, property_value_content: str = "", parent=None):
        super().__init__(parent)  
        self.row_id = row_id # Unique identifier for this specific row widget
        self.property_key_content = property_key_content
        self.property_type = property_type
        self.property_value_content = property_value_content
        print(f"Creating CustomRowWidget for row {self.row_id} with property type '{self.property_type}' and value '{self.property_value_content}'")

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
        self.property_key.setText(property_key_content) 
        self.property_key .setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.property_key.setFixedSize(100, 25)
        
        self.menu1 = self._create_menu1() 
        self.property_key.setMenu(self.menu1)  

        # Create Property Value 
        self.property_value = QLineEdit(f"Data for {row_id}")
        self.property_value.setText(property_value_content)   

        # Add widgets to row's horizontal layout
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.property_key)
        self.layout.addWidget(self.property_value) 
    
    def _create_menu1(self):
        """
        Declutters __init__.
        Creates the first menu with basic options.
        """
        menu1 = QMenu(self) 

        # Visual indicator of what this property is
        property_label = QAction(f"Type: {self.property_type.capitalize().replace('_', ' ')}", self) 
        menu1.addAction(property_label)

        menu2 = self.edit_property(self.property_type)
  
        menu2.setTitle("Edit Property Type")
        menu2.setToolTip("Edit Property Type")
        menu1.addMenu(menu2) 
 
        menu1.addSeparator()        
        options_visibility = QAction("Property Visibility", self)
        options_visibility.triggered.connect(lambda: print(f"Property Visibility in row {self.row_id} clicked!"))
        menu1.addAction(options_visibility)
        
        options_duplicate = QAction("Duplicate Property", self)
        options_duplicate.triggered.connect(lambda: print(f"Duplicate Property in row {self.row_id} clicked!"))
        menu1.addAction(options_duplicate)
        
        options_delete = QAction("Delete Property", self)
        options_delete.triggered.connect(lambda: self.delete_requested.emit(self.row_id))
        menu1.addAction(options_delete)

        return menu1
    
    def edit_property(self, property_type):
        """
        Cascading menu from Menu 1.
        Changes based on type.
        Will have further functions for this.
        """ 
        if property_type == "text":
            menu2 = self.edit_property_text()
        elif property_type == "number":
            menu2 = self.edit_property_number()
        elif property_type == "select":
            menu2 = self.edit_property_select()
        elif property_type == "multi_select":
            menu2 = self.edit_property_multi_select()
        elif property_type == "checkbox":
            menu2 = self.edit_property_checkbox()
        
        return menu2
    
    def _change_type(self, type="text"): 
        """
        @param type: Type of property to add.
        - text, number, select, multi_select, checkbox
        """ 
        old = self.property_type
        self.property_type=type
        self.value_changed_requested.emit(self.row_id, self.property_key.text(), self.property_type, self.property_value.text())
        self._rename_property_key(new_key=self.property_key.text())  # Update the property key
        self.menu1 = self._create_menu1()  # Recreate the menu with the new type
        print(f"Property type changed from {old} to '{self.property_type}' for row {self.row_id}")


    def _generate_types(self):
        """
        Generates a menu for changing property type.
        """
        menu_change_type = QMenu(self)
        for property_type in TYPES_OF_PROPERTIES: 
            property_text = property_type.capitalize().replace('_', ' ')
            options_text = QAction(property_text, self) 
            options_text.triggered.connect(lambda checked, t=property_type: self._change_type(type=t)) 
            menu_change_type.addAction(options_text) 
        
        menu_change_type.setTitle("Change Type")
        menu_change_type.setToolTip("Change Property Type")

        return menu_change_type
    
    def _rename_property_key(self, new_key):
        """
        Renames the property key.
        """
        self.property_key.setText(new_key) 


    def edit_property_text(self):
        """
        Creates a menu for text property type.
        """
        menu = QMenu(self)

        menu_change_type = self._generate_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Text Property", self)
        options_text.triggered.connect(lambda: print(f"Text Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)
        
        options_text = QAction("Edit Text Property", self)
        options_text.triggered.connect(lambda: print(f"Edit Text Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 
    
    def edit_property_number(self):
        """
        Creates a menu for text property type.
        """
        menu = QMenu(self)

        menu_change_type = self._generate_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Number Property", self)
        options_text.triggered.connect(lambda: print(f"Number Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)
        
        options_text = QAction("Edit Number Property", self)
        options_text.triggered.connect(lambda: print(f"Edit Number Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 
    
    def edit_property_select(self):
        """
        Creates a menu for text property type.
        """
        menu = QMenu(self)

        menu_change_type = self._generate_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Select Property", self)
        options_text.triggered.connect(lambda: print(f"Number Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)
        
        options_text = QAction("Edit Select Property", self)
        options_text.triggered.connect(lambda: print(f"Edit Number Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 
    
    def edit_property_multi_select(self):
        """
        Creates a menu for text property type.
        """
        menu = QMenu(self)

        menu_change_type = self._generate_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Multi Select Property", self)
        options_text.triggered.connect(lambda: print(f"Multi Select Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)
        
        options_text = QAction("Edit Multi Select Property", self)
        options_text.triggered.connect(lambda: print(f"Edit Multi Select Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 
    
    def edit_property_checkbox(self):
        """
        Creates a menu for text property type.
        """
        menu = QMenu(self)

        menu_change_type = self._generate_types()
        menu.addMenu(menu_change_type) 
        
        options_text = QAction("Checkbox Property", self)
        options_text.triggered.connect(lambda: print(f"Checkbox Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)
        
        options_text = QAction("Edit Checkbox Property", self)
        options_text.triggered.connect(lambda: print(f"Edit Checkbox Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 
     