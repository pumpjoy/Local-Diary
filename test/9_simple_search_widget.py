# A simple Search Widget Example
# Generated with Gemini 2.5 Flash
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QToolButton, 
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

class CombinedSearchWidget(QWidget):
    """A custom widget combining a QToolButton and a QLineEdit."""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create a horizontal layout for the components
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0) # Remove internal spacing
        self.layout.setSpacing(0) # Remove spacing between widgets

        # Create the QToolButton
        self.tool_button = QToolButton(self)
        self.tool_button.setIcon(QIcon.fromTheme("search")) # Use a standard icon
        
        # Optional: Set a tooltip or default action
        self.search_action = QAction("Search", self)
        self.search_action.setIcon(QIcon.fromTheme("search"))
        self.search_action.triggered.connect(self.handle_search)
        self.tool_button.setDefaultAction(self.search_action)
        self.tool_button.setToolTip("Click to perform search")

        # Create the QLineEdit
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Enter search query...")
        self.line_edit.setFrame(False) # This is key for a seamless look

        # Add widgets to the layout
        self.layout.addWidget(self.tool_button)
        self.layout.addWidget(self.line_edit)
        
        # Apply styling to the container widget to create a unified border
        self.setStyleSheet("""
            QWidget {
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                background-color: white;
            }
            QLineEdit {
                background-color: transparent; /* Match parent background */
                border: none;
            }
            QToolButton {
                border: none;
                background-color: transparent; /* Match parent background */
            }
        """)

    def handle_search(self):
        query = self.line_edit.text()
        print(f"Searching for: {query}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combined Widget Example")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Use the custom CombinedSearchWidget
        self.search_widget = CombinedSearchWidget()
        main_layout.addWidget(self.search_widget)
        
        main_layout.addStretch(1)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Ensure QIcon.fromTheme works, though it might not have the 'search' icon on all systems
    QIcon.setFallbackThemeName("Breeze") # Optional fallback
    window = MainWindow()
    window.show()
    sys.exit(app.exec())