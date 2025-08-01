# Cascading Menu Example
# Generated with Gemini 2.5 Flash
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow, QVBoxLayout,
    QWidget, QToolButton, QMenu,)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cascading Menu Example")
        self.setGeometry(100, 100, 400, 300)

        # Set up a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.tool_button = QToolButton(self)
        self.tool_button.setText("Main Menu")

        self.tool_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.menu1 = QMenu(self)
        self.menu2 = QMenu(self)

        action2_1 = QAction("Action 2.1", self)
        action2_2 = QAction("Action 2.2", self)
        self.menu2.addAction(action2_1)
        self.menu2.addAction(action2_2)

        self.menu1.addMenu(self.menu2)
        self.menu1.addSeparator()
         
        action1_1 = QAction("Action 1.1", self)
        self.menu1.addAction(action1_1)
        self.tool_button.setMenu(self.menu1)
 
        action2_1.triggered.connect(self.on_action_2_1_triggered)
        action1_1.triggered.connect(self.on_action_1_1_triggered)
 
        layout.addWidget(self.tool_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_action_1_1_triggered(self):
        print("Action 1.1 triggered!")

    def on_action_2_1_triggered(self):
        print("Action 2.1 triggered!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())