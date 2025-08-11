from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout, QHBoxLayout, QGridLayout, 
    QWidget, QWidgetAction, QStackedWidget,
    QLabel, QToolButton,  QLineEdit, QPushButton, 
    QScrollArea, QMenu, 
)
from PyQt6.QtGui import QAction, QIntValidator 

from asset.css_cheatsheet import ( 
    PROPERTY_OPTIONS_COLOUR_HEX
)

class MenuOptionWidget(QWidget):
    """ 
    For M/Select and Status
    Represents 1 option of a single property_id
    Has an Up button, Down button and A QToolButton/QLabel (OptionWord)
    QToolButton/QLabel based on edit_mode.
    """
    
    def __init__(self,
                 row_id: int,
                 property_id: int,
                 property_type: str,
                 property_value: str, 
                 parent=None):
        super().__init__(parent)

        self.property_id = property_id
        self.property_type = property_type
        self.property_value = property_value 
        self.row_id = row_id

        self.current_row_id = 0
        self.current_order = []
        self.dict_row_options = {}

        self.main_layout = QVBoxLayout(self)

        self.header = QHBoxLayout()

        # Label showing Options
        label = QLabel("Options")

        # Add New property_value
        bt_add_new = QToolButton('+') # TODO: Placeholder, add icon
        bt_add_new.setToolTip("Add new option")
        bt_add_new.setCursor(Qt.CursorShape.CrossCursor)
        bt_add_new.setFixedSize(30, 30)
        bt_add_new.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        bt_add_new.setStyleSheet(f"margin: 5px;")
        bt_add_new.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        menu_line_edit_property_value = QMenu(self)
        bt_add_new.setMenu(menu_line_edit_property_value)

        line_edit_property_value = QLineEdit()
        line_edit_property_value.returnPressed.connect(self._add_new_row)

        line_edit_action = QWidgetAction(menu_line_edit_property_value)
        line_edit_action.setDefaultWidget(line_edit_property_value)
        menu_line_edit_property_value.addAction(line_edit_action)

        self.header.addWidget(label)
        self.header.addWidget(bt_add_new)
    
        # -----------------------------------------------
        # Actual Scroll Area with options/property_values
        self.grid_scroll_area = QScrollArea(self)
        self.grid_scroll_area.setWidgetResizable(True)
        self.grid_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.grid_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.view_scroll_content_widget = QWidget(self.grid_scroll_area)
        self.view_scroll_content_layout = QVBoxLayout(self.view_scroll_content_widget)
        self.view_scroll_content_layout.setContentsMargins(5, 5, 5, 5)
        self.view_scroll_content_layout.setSpacing(5)

        # Actual content
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        self.view_scroll_content_layout.addLayout(self.content_layout)
        self.view_scroll_content_layout.addStretch(1)

        self.grid_scroll_area.setWidget(self.view_scroll_content_widget)

        # -----------------------------------------------
        self.main_layout.addLayout(self.header)
        self.main_layout.addWidget(self.grid_scroll_area, 1)
        self.main_layout.stretch(1)

    def _load_rows(self):
        """Loads rows based on PropertyOptionWidget"""
        loaded_data = self.property_option_manager.get_setting('')
        pass

    def _add_new_row(self):
        row_id = self.current_row_id
        while row_id in self.dict_row_options:
            row_id += 1
        self.current_row_id = row_id + 1

        option_row = MenuOptionRows(row_id)

        self.dict_row_options[row_id] = option_row

        option_row.requested_option_move_up.connect()
        option_row.requested_option_move_down.connect()
        option_row.requested_option_delete.connect()
        option_row.requested_option_value_changed.connect()
        option_row.requested_option_colour_changed.connect()
 
        self.current_order.append(row_id)
        self.view_scroll_content_layout.addWidget(option_row)
 
    # --- Option request actions ---
    def move_row_up(self):
        current_order_ids = self._get_current_order()
        try:
            pass
        except ValueError:
            print(f"MenuOptionWidget: Error: Row with ID ")
        pass

    def move_row_down(self):
        pass

    def delete_row(self):
        pass
    def value_changed(self):
        """Update said property_value. Also on PropertyOptionManager"""
        pass

    # --- Supporting functions ---
    def _get_current_order(self) -> list[int]:
        """
        Inspects QGridLayout to determine current visual order
        of CustomRowWidget instances by their row_id.
        This list represents logical order of rows.
        """
        order = []
        self.content_layout
        # Iterate through all rows in grid layout
        for r in range(self.content_layout.rowCount()):
            # Get item in first column of current row
            item = self.content_layout.itemAtPosition(r, 0)
            if item and item.widget():
                widget = item.widget()
                # If it's a CustomRowWidget, add its row_id to order list
                if isinstance(widget, MenuOptionRows):
                    # order.append(widget.property_id)
                    # Find the row_id for this widget
                    for row_id, w in self.dict_row_options.items():
                        if w is widget:
                            order.append(row_id)
                            break
        return order

class MenuOptionRows(QWidget):

    requested_option_move_up = pyqtSignal(int)
    requested_option_move_down = pyqtSignal(int)
    requested_option_delete = pyqtSignal(int)
    requested_option_value_changed = pyqtSignal(int, str) # Name change
    requested_option_colour_changed = pyqtSignal(int, str) # Name change
    
    def __init__(self,
                 row_id: int,
                 property_value: str, 
                 parent=None):
        super().__init__(parent)
        
        self.row_id = row_id
        self.property_value = property_value 
        
        # Set up horizontal layout for this row's widgets
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0) 
        self.layout.setSpacing(5)

        # Create 'Up' button
        self.up_button = QPushButton("▲") # Placeholder for button
        self.up_button.setFixedSize(30, 25) 
        self.up_button.clicked.connect(lambda: self.requested_option_move_up.emit(self.row_id))

        # Create 'Down' button
        self.down_button = QPushButton("▼") # Placeholder for button
        self.down_button.setFixedSize(30, 25)   
        self.down_button.clicked.connect(lambda: self.requested_option_move_down.emit(self.row_id))

        # Create property_value extra menu
        self.option_word = QToolButton()
        self.option_word.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.option_word.setText(self.property_value)
        self.option_word_menu = QMenu(self)
        
        ### Option menu 1: property_value edit
        self.option_line_edit = QLineEdit()

        ### Option menu 2: Delete property_value
        self.option_word_menu_delete = QAction("Delete") 
        self.option_word_menu_delete.triggered.connect(lambda: self.requested_option_delete.emit(self.row_id))
        self.option_word.addAction(self.option_word_menu_delete)

        self.option_word_menu.addSeparator()

        ### Option menu 3: property_value colour picker
        self.colour_grid = QGridLayout()
        self.colour_grid.setSpacing(10)
        rows = 5
        cols = 2
        # Colour selection
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                if index < len(PROPERTY_OPTIONS_COLOUR_HEX):
                    colour = PROPERTY_OPTIONS_COLOUR_HEX[index]
                    button = QPushButton()
                    button_size = 50 # TODO: Temporarily 
                    button.setFixedSize(QSize(button_size, button_size))
                    button.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {colour};
                            border: 2px solid #555;
                            border-radius: {button_size / 2}px;
                        }}
                        QPushButton:hover {{
                            border: 2px solid white;
                        }}
                    """)
                    button.clicked.connect(lambda _, c=colour: self.on_color_selected(c))
                    self.colour_grid.addWidget(button, row, col) 
        
        self.option_word.setText(self.property_value)
        self.option_word.setFixedSize(100, 25)

        pass