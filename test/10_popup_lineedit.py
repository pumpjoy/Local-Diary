# QToolButton with Pop-up LineEdit Example
# This example demonstrates how to create a QToolButton that opens a pop-up menu with a
# Generated with Gemini 2.5 Flash
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolButton,
    QMenu,
    QLineEdit,
    QWidgetAction,
    QMessageBox,
    QWidget,
    QVBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class SearchButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
 
        self.setIcon(QIcon.fromTheme("search"))
        self.setToolTip("Search")
        
        self.setup_menu()

    def setup_menu(self): 
        self.search_menu = QMenu(self)
         
        self.line_edit = QLineEdit(self.search_menu)
        self.line_edit.setPlaceholderText("Enter search query...")
         
        self.line_edit.returnPressed.connect(self.perform_search)
         
        self.search_action = QWidgetAction(self.search_menu)
        
        self.search_action.setDefaultWidget(self.line_edit)
         
        self.search_menu.addAction(self.search_action)
 
        self.setMenu(self.search_menu)
    
    def showMenu(self):
        """
        Overriding showMenu to give focus to the QLineEdit when the menu is shown.
        """
        super().showMenu()
        self.line_edit.setFocus()

    def perform_search(self):
        query = self.line_edit.text()
        if query:
            self.search_menu.hide()
            self.line_edit.clear()
            
            QMessageBox.information(self, "Search", f"Searching for: {query}")
        else:
            QMessageBox.warning(self, "Search", "Please enter a search query.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToolButton with Pop-up LineEdit")
        self.setGeometry(100, 100, 300, 150)
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        self.search_button = SearchButton(self)
        
        layout.addWidget(self.search_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())