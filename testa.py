import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu
from PyQt6.QtGui import QAction # Corrected import
from PyQt6.QtCore import pyqtSignal

class RecentMenu(QMenu):
    """A custom widget for the 'Open Recent' menu."""

    # Define a custom signal to emit the selected file name
    fileSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__("Open Recent", parent)
        self.populate_menu([]) # Initialize with an empty list

    def populate_menu(self, recent_files):
        """Populates the menu with a list of recent files."""
        # Clear existing actions to prevent duplicates
        self.clear()

        if not recent_files:
            # Add a disabled action if there are no recent files
            no_files_action = QAction("No recent files", self)
            no_files_action.setDisabled(True)
            self.addAction(no_files_action)
            return

        for file_path in recent_files:
            # Create an action for each file
            action = QAction(file_path, self)
            # Connect the action's triggered signal to a slot
            action.triggered.connect(lambda checked, f=file_path: self.on_file_selected(f))
            self.addAction(action)

    def on_file_selected(self, file_path):
        """Emits the fileSelected signal."""
        self.fileSelected.emit(file_path)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Recent Menu Example")
        self.setGeometry(100, 100, 400, 300)

        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        # Create an instance of the custom RecentMenu widget
        self.recent_menu = RecentMenu(self)

        # Add the custom RecentMenu widget to the parent menu
        file_menu.addMenu(self.recent_menu)

        # Connect the custom signal to a slot in the main window
        self.recent_menu.fileSelected.connect(self.open_file)

        # Simulate populating the menu with recent files
        recent_files_list = ["C:/Users/User/docs/report.docx", "D:/Projects/app.py", "E:/Photos/vacation.jpg"]
        self.recent_menu.populate_menu(recent_files_list)

    def open_file(self, file_path):
        print(f"Opening file: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())