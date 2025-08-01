from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QToolButton, QLabel, QLineEdit, QPushButton, QDateEdit, 
    QScrollArea, QMenu, QMessageBox,
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QDate

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

    def __init__(self, row_id: int, property_key_content: str, property_type: str, property_value_content: str = "", parent=None):
        super().__init__(parent)
        self.row_id = row_id # Unique identifier for this specific row widget
        self.property_key_content = property_key_content
        self.property_type = property_type
        self.property_value_content = property_value_content

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
        self.current_menu = 1 

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
        options_text = QAction("Edit Property", self)
        options_text.triggered.connect(lambda: self._create_menu2(type))
        menu1.addAction(options_text)
        menu1.addSeparator()        
        options_number = QAction("Property Visibility", self)
        options_number.triggered.connect(lambda: print(f"Property Visibility in row {self.row_id} clicked!"))
        menu1.addAction(options_number)
        
        options_text = QAction("Duplicate Property", self)
        options_text.triggered.connect(lambda: print(f"Duplicate Property in row {self.row_id} clicked!"))
        menu1.addAction(options_text)
        
        options_text = QAction("Delete Property", self)
        options_text.triggered.connect(lambda: self.delete_requested.emit(self.row_id))
        menu1.addAction(options_text)

        return menu1
    
    def _create_menu2(self, type):
        """
        Cascading menu from Menu 1.
        Changes based on type.
        Will have further functions for this.
        """
        menu2 = QMenu(self)
        if type == "text":
            return self.create_menu_text()
        # elif type == "number":
        #     return self.create_menu_number()
        # elif type == "select":
        #     return self.create_menu_select()
        # elif type == "multi_select":
        #     return self.create_menu_multi_select()
        # elif type == "checkbox":
        #     return self.create_menu_checkbox()
        
        
        return menu2
    
    def create_menu_text(self):
        """
        Creates a menu for text property type.
        """
        menu = QMenu(self)
        options_text = QAction("Text Property", self)
        options_text.triggered.connect(lambda: print(f"Text Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)
        
        options_text = QAction("Edit Text Property", self)
        options_text.triggered.connect(lambda: print(f"Edit Text Property in row {self.row_id} clicked!"))
        menu.addAction(options_text)

        return menu 