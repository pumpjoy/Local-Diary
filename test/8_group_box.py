# A GroupBox Example
# Generated with Gemini 2.5 Flash
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QGroupBox, 
) 

class BoxWithElementsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Box with Button and Numbers")
        self.setGeometry(100, 100, 400, 250)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.init_ui()

    def init_ui(self):
        # Create the QGroupBox to serve as the "box"
        self.my_box = QGroupBox("My Custom Box") # You can give it a title
        self.main_layout.addWidget(self.my_box)

        # Create a vertical layout inside the QGroupBox
        # This will hold the top row (button & numbers) and any other content below
        self.box_v_layout = QVBoxLayout(self.my_box)

        # Create the top horizontal layout for the button and numbers
        self.top_h_layout = QHBoxLayout()

        # 1. Button on the top-left
        self.my_button = QPushButton("Click Me!")
        self.my_button.setFixedSize(80, 30) # Optional: set a fixed size
        self.my_button.clicked.connect(self.on_button_click)
        self.top_h_layout.addWidget(self.my_button)

        # Add a horizontal spacer to push the numbers to the right
        self.top_h_layout.addStretch(1) # Stretch factor of 1 means it expands as much as possible

        # 2. Two numbers on the top-right
        self.number1_label = QLabel("123")
        self.number1_label.setStyleSheet("font-size: 16px; font-weight: bold; color: blue;")
        self.number2_label = QLabel("456")
        self.number2_label.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")

        # Use another QHBoxLayout to group the numbers tightly
        self.numbers_h_layout = QHBoxLayout()
        self.numbers_h_layout.addWidget(self.number1_label)
        self.numbers_h_layout.addWidget(self.number2_label)
        
        # Add a small fixed space between the numbers if desired
        self.numbers_h_layout.addSpacing(10) 
        
        # Add the numbers layout to the top horizontal layout
        self.top_h_layout.addLayout(self.numbers_h_layout)

        # Add the top horizontal layout to the box's vertical layout
        self.box_v_layout.addLayout(self.top_h_layout)

        # (Optional) Add some more content below the top row
        self.box_v_layout.addWidget(QLabel("This is some content inside the box."))
        self.box_v_layout.addWidget(QLabel("You can put more widgets here."))

        # Add a stretch at the bottom of the box's layout to push content to the top
        self.box_v_layout.addStretch(1)

    def on_button_click(self):
        print("Button clicked!")
        # You could update the numbers here, for example:
        import random
        self.number1_label.setText(str(random.randint(1, 999)))
        self.number2_label.setText(str(random.randint(1, 999)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BoxWithElementsApp()
    window.show()
    sys.exit(app.exec())