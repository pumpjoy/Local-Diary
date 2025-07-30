# Test to have buttons generate some labels.
# Yes the label is clickable.

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

class ClickableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print("Label clicked!")

class DynamicWidgetGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dynamic Widget Generator')
         
        self.layout = QVBoxLayout()
 
        self.add_button = QPushButton('Add Label', self)
        self.remove_button = QPushButton('Remove Last Label', self)

        self.add_button.clicked.connect(self.add_label)
        self.remove_button.clicked.connect(self.remove_label)
         
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
         
        self.clickable_label = ClickableLabel('Click Me!', self)
        
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.clickable_label)
 
        self.setLayout(self.layout)

    def add_label(self): 
        label = ClickableLabel(f'New Label {self.layout.count()-1}', self)
         
        self.layout.addWidget(label)

    def remove_label(self):
        # Remove the last widget if it exists and is not the buttons
        if len(self.layout) > 1:
            self.layout.takeAt(len(self.layout) - 1).widget().deleteLater()
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DynamicWidgetGenerator()
    window.show()
    sys.exit(app.exec())
