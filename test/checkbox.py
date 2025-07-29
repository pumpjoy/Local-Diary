# Example: Checkbox in PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel

app = QApplication([])

window = QWidget()
layout = QVBoxLayout()

checkbox = QCheckBox("Check me!")
label = QLabel("Unchecked")

def on_state_changed(state):
    if state:
        label.setText("Checked")
    else:
        label.setText("Unchecked")

checkbox.stateChanged.connect(on_state_changed)

layout.addWidget(checkbox)
layout.addWidget(label)
window.setLayout(layout)
window.show()

app.exec()