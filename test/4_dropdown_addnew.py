from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QGridLayout, QPushButton, QLineEdit, QMenu, QToolButton
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import sys

class DynamicGridExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Grid Layout Example with Menu")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(10)

        self.current_row = 0
        self.add_new_row_button(self.current_row)

    def add_new_row_button(self, row_index):
        """Adds a new row with an 'Add New' button that has an options menu."""
        
        button = QToolButton()
        button.setText("Add New")
        button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup) # Shows a separate arrow for the menu

        menu = QMenu(self) 
        
        transform_action = QAction("Transform Row", self)
        transform_action.triggered.connect(lambda: self.transform_row(row_index))
        menu.addAction(transform_action)

        another_action = QAction("Do Something Else", self)
        another_action.triggered.connect(lambda: self.do_something_else(row_index))
        menu.addAction(another_action)

        # Set the menu to the button
        button.setMenu(menu)

        self.grid_layout.addWidget(button, row_index, 0, 1, 2) # Span 2 columns initially
        self.current_row = row_index + 1

    def transform_row(self, row_index):
        """
        Transforms the specified row based on the clicked menu action:
        - Changes the "Add New" tool button to a "Text" button.
        - Adds a QLineEdit in the second column.
        - Adds a new "Add New" tool button in the next row.
        """
        button_to_remove = None
        for i in range(self.grid_layout.columnCount()):
            item = self.grid_layout.itemAtPosition(row_index, i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QToolButton) and widget.text() == "Add New":
                    button_to_remove = widget
                    break
        
        if button_to_remove:
            self.grid_layout.removeWidget(button_to_remove)
            button_to_remove.deleteLater()

        text_button = QPushButton("Text")
        text_button.clicked.connect(lambda: print(f"Text button in row {row_index} clicked!"))
        self.grid_layout.addWidget(text_button, row_index, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        line_edit = QLineEdit()
        self.grid_layout.addWidget(line_edit, row_index, 1)

        self.add_new_row_button(self.current_row)

    def do_something_else(self, row_index):
        """A placeholder for another action from the menu."""
        print(f"Action 'Do Something Else' triggered for row {row_index}")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicGridExample()
    window.show()
    sys.exit(app.exec())