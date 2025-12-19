from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout,
    QWidget, QWidgetAction, QStackedWidget,
    QToolButton,  QLineEdit, QPushButton, 
    QMenu, 
)
from PyQt6.QtGui import QAction, QIntValidator 

from asset.css_cheatsheet import TYPES_OF_PROPERTIES 
from asset.menu_option_widget import MenuOptionWidget

class MenuEditProperty(QMenu):
    """
    A custom widget that displays options available in this property.
    Dynamically generates MenuOptionWidget based on
    PropertyOptionManager - property_id and property_type.
    
    Is a Menu slot for CustomRowWidget
    """

    requested_menu_key_change = pyqtSignal(str) 
    requested_menu_type_change = pyqtSignal(int, str) 
    requested_menu_value_change = pyqtSignal(int, str) 


    def __init__(self,
                 property_id,
                 property_key,
                 property_type,
                 property_value,
                 parent=None):
        super().__init__(parent)
        self.property_id = property_id 
        self.property_key = property_key
        self.property_type = property_type
        self.property_value = property_value 
        self.setTitle("Edit Properties")
    
    # --- Per type ---
    ### Text
    def _setup_edit_text_ui(self):
        """Edit-mode: Text UI"""
        self._common_menu_items()

    ### Number
    def _setup_edit_number_ui(self):
        """Edit-mode: Number UI"""
        self._common_menu_items()

    ### Select
    def _setup_edit_select_ui(self):
        """Edit-mode: M/Select Properties UI
        Can edit name of Property_value and change colour using picker.
        """
        self._common_menu_items()
 
        menu_option_viewer = MenuOptionWidget()
        menu_option_widget = QWidgetAction(menu_option_viewer)
        self.addAction(menu_option_widget)
    
    
    # ------ Common ------
    def _common_menu_items(self):
        """Creates the line edit and a menu for property type change, and separator"""

        # Line Edit to change property_key/Name
        self.linedit_name = QLineEdit()
        self.linedit_name.setText(self.property_key)
        self.linedit_name.returnPressed.connect(self.on_lineedit_enter_pressed)
        lineedit_name_action = QWidgetAction(self)
        lineedit_name_action.setDefaultWidget(self.linedit_name)
        self.addAction(lineedit_name_action)

        # Menu Property Type changer
        menu_property_type_change = self._generate_menu_types()
        self.addMenu(menu_property_type_change)

        # Separator
        self.addSeparator() 

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
    
    # --- Functions for calling update --- 
    def on_lineedit_enter_pressed(self):
        """Edits property_key"""
        text = self.linedit_name.text()

        # Updates property_value with entered text
        self.property_key = text 
        self.requested_menu_key_change.emit(self.property_key)

    def _set_row_type(self, new_type: str):
        """
        Updates the row's type and all associated UI elements.
        Switches the visible widget in the self.content_stack based on the row's type.
        """
        if self.property_type != new_type:
            self.property_type = new_type
            self.requested_menu_type_change.emit(self.property_id, self.property_type)