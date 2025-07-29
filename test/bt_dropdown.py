import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMenu, QLineEdit
)
from PyQt6.QtGui import QAction # QAction is usually imported from QtGui

class DropdownButtonExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt Drop-down Button Example")
        self.setGeometry(100, 100, 400, 200)

        main_layout = QVBoxLayout(self)

        self.status_label = QLineEdit("No action selected yet.")
        self.status_label.setReadOnly(True)
        main_layout.addWidget(self.status_label)

        # 1. Create the QPushButton
        self.dropdown_button = QPushButton("Options")
        main_layout.addWidget(self.dropdown_button)

        # 2. Create the QMenu
        options_menu = QMenu(self)

        # 3. Create QActions and add them to the menu
        action1 = QAction("Save", self)
        action1.triggered.connect(lambda: self.update_status("Save action triggered!"))
        options_menu.addAction(action1)

        action2 = QAction("Load", self)
        action2.triggered.connect(lambda: self.update_status("Load action triggered!"))
        options_menu.addAction(action2)

        options_menu.addSeparator() # Add a separator line

        action3 = QAction("Settings...", self)
        action3.triggered.connect(lambda: self.update_status("Settings action triggered!"))
        options_menu.addAction(action3)

        # 4. Attach the QMenu to the QPushButton
        self.dropdown_button.setMenu(options_menu)

        main_layout.addStretch()

    def update_status(self, message):
        self.status_label.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropdownButtonExample()
    window.show()
    sys.exit(app.exec())