from PyQt6.QtWidgets import (
    QApplication, QWidget,  # Changed QMainWindow to QWidget
    QGridLayout, QPushButton, QLineEdit, QMenu, QToolButton,
    QHBoxLayout
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal
import sys

# --- Custom Row Widget ---
class CustomRowWidget(QWidget):
    """
    A custom widget representing a single row in grid,
    containing Up/Down buttons, a text button, and a line edit.
    It emits signals when its Up/Down buttons are clicked.
    """
    move_up_requested = pyqtSignal(int)    # Signal: emitted when 'Up' button is clicked (passes row_id)
    move_down_requested = pyqtSignal(int)  # Signal: emitted when 'Down' button is clicked (passes row_id)

    def __init__(self, row_id: int, text_content: str, parent=None):
        super().__init__(parent)
        self.row_id = row_id # Unique identifier for this specific row widget

        # Set up horizontal layout for this row's widgets
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5) # Add some padding around row
        self.layout.setSpacing(5) # Spacing between widgets in this row

        # Create 'Up' button
        self.up_button = QPushButton("▲") # Unicode Up Arrow
        self.up_button.setFixedSize(25, 25) # Fixed size for a compact button
        # Connect 'Up' button to emit its custom signal
        self.up_button.clicked.connect(lambda: self.move_up_requested.emit(self.row_id))

        # Create 'Down' button
        self.down_button = QPushButton("▼") # Unicode Down Arrow
        self.down_button.setFixedSize(25, 25) # Fixed size for a compact button
        # Connect 'Down' button to emit its custom signal
        self.down_button.clicked.connect(lambda: self.move_down_requested.emit(self.row_id))

        # Create 'Text' button (as requested, a button instead of a QLabel)
        self.text_button = QPushButton(text_content)

        # Create Line Edit
        self.line_edit = QLineEdit(f"Data for {row_id}")

        # Add widgets to row's horizontal layout
        self.layout.addWidget(self.up_button)
        self.layout.addWidget(self.down_button)
        self.layout.addWidget(self.text_button)
        self.layout.addWidget(self.line_edit)

# --- Main Window / Top-level Widget ---
class DynamicGridExample(QWidget): # Changed base class from QMainWindow to QWidget
    """
    Top-level QWidget managing a QGridLayout with dynamic, reorderable rows.
    Each reorderable row contains up/down buttons, a text button, and a line edit.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Grid Layout with Up/Down Buttons")
        self.setGeometry(100, 100, 500, 400) # Still works for a top-level QWidget

        # No central_widget is needed when inheriting from QWidget directly.
        # Apply QGridLayout directly to 'self'.
        self.grid_layout = QGridLayout(self) 
        self.grid_layout.setContentsMargins(10, 10, 10, 10) # Margins around grid
        self.grid_layout.setSpacing(10) # Spacing between cells in grid

        # Dictionary to store CustomRowWidget instances, mapped by their unique row_id.
        self.row_widgets_by_id = {} 
        self.next_row_id = 0      # Counter for generating unique row_ids

        # Reference to "Add New" button widget.
        self.add_new_button_widget = None 
        self.add_new_row_button() # Create and initially place "Add New" button

        # Add some initial  rows for demonstration purposes
        self.add_row("First Item")
        self.add_row("Second Item")
        self.add_row("Third Item")

        # After initial setup, update state of Up/Down buttons
        self.update_button_states()

    def add_new_row_button(self):
        """
        Creates 'Add New' QToolButton with its action menu.
        This button is responsible for adding new rows.
        It will always be placed at the very bottom of grid.
        """
        add_button = QToolButton()
        add_button.setText("Add New")
        add_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup) 

        menu = QMenu(self) 
        add_generic_action = QAction("Add Generic Row", self)
        add_generic_action.triggered.connect(lambda: self.add_row(f"New Item {self.next_row_id}"))
        menu.addAction(add_generic_action)
        add_button.setMenu(menu)

        self.add_new_button_widget = add_button 

        self._rebuild_layout_from_order(self._get_current_row_order())


    def add_row(self, text_content: str):
        """
        Creates a new CustomRowWidget and adds it to grid.
        new row is always added just above 'Add New' button.
        """
        row_id = self.next_row_id
        self.next_row_id += 1

        custom_row_widget = CustomRowWidget(row_id, text_content, self) # Parent is 'self'
        self.row_widgets_by_id[row_id] = custom_row_widget
        
        custom_row_widget.move_up_requested.connect(self.move_row_up)
        custom_row_widget.move_down_requested.connect(self.move_row_down)

        self._rebuild_layout_from_order(self._get_current_row_order() + [row_id])


    def _get_current_row_order(self) -> list[int]:
        """
        Inspects QGridLayout to determine current visual order
        of CustomRowWidget instances by their row_id.
        """
        order = []
        for r in range(self.grid_layout.rowCount()):
            item = self.grid_layout.itemAtPosition(r, 0)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, CustomRowWidget):
                    order.append(widget.row_id)
        return order


    def move_row_up(self, row_id_to_move: int):
        """
        Moves CustomRowWidget with given row_id up one position.
        """
        current_order_ids = self._get_current_row_order()
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
        """
        Moves CustomRowWidget with given row_id down one position.
        """
        current_order_ids = self._get_current_row_order()
        try:
            current_index = current_order_ids.index(row_id_to_move)
            if current_index < len(current_order_ids) - 1:
                current_order_ids[current_index], current_order_ids[current_index + 1] = \
                    current_order_ids[current_index + 1], current_order_ids[current_index]
                self._rebuild_layout_from_order(current_order_ids)

        except ValueError:
            print(f"Error: Row with ID {row_id_to_move} not found in current order.")
            
        self.update_button_states()


    def _rebuild_layout_from_order(self, new_order_ids: list[int]):
        """
        Clears entire QGridLayout and then re-adds all widgets
        (Custom Widget Rows and 'Add New' button) in specified new order.
        """
        # Remove all widgets from layout.
        # Widgets are detached (setParent(None)) but not deleted here as they are reused.
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None) 

        # Re-add CustomRowWidget instances based on new_order_ids list.
        current_grid_row = 0
        for row_id in new_order_ids:
            widget = self.row_widgets_by_id[row_id]
            self.grid_layout.addWidget(widget, current_grid_row, 0, 1, self.grid_layout.columnCount())
            current_grid_row += 1
        
        # Re-add "Add New" button at the very last row.
        if self.add_new_button_widget:
            self.grid_layout.addWidget(self.add_new_button_widget, current_grid_row, 0, 1, self.grid_layout.columnCount())
        
        self.grid_layout.update()


    def update_button_states(self):
        """
        Enables/disables 'Up' and 'Down' buttons based on their current position.
        """
        current_order_ids = self._get_current_row_order()
        num_rows = len(current_order_ids)

        for i, row_id in enumerate(current_order_ids):
            widget = self.row_widgets_by_id[row_id]
            widget.up_button.setEnabled(i > 0) 
            widget.down_button.setEnabled(i < num_rows - 1)


# --- Application Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = DynamicGridExample() # Now it's a QWidget acting as top-level window
    window.show() 
    sys.exit(app.exec())