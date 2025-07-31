import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QDateEdit, 
    QLabel,
)
from PyQt6.QtCore import QDate

class DateSelectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Date Selector")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.init_ui()

    def init_ui(self): 
        self.date_edit = QDateEdit(self)
         
        self.date_edit.setDate(QDate.currentDate()) 

        # Set the display format 
        # Common formats: "dd/MM/yyyy", "MMMM d, yyyy", "yyyy-MM-dd"
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
 
        self.date_edit.setCalendarPopup(True)
 
        self.date_edit.setMinimumDate(QDate(1900, 1, 1))
        self.date_edit.setMaximumDate(QDate(2100, 12, 31))

        self.layout.addWidget(QLabel("Select a Date:"))
        self.layout.addWidget(self.date_edit)
 
        self.selected_date_label = QLabel("No date selected yet.")
        self.layout.addWidget(self.selected_date_label)
 
        self.date_edit.dateChanged.connect(self.update_label_on_change) 
 

    def update_label_on_change(self, qdate_obj):
        # Updates the label whenever the date in QDateEdit changes
        pydate_obj = qdate_obj.toPyDate()
        self.selected_date_label.setText(f"Current Date: {pydate_obj.strftime('%d-%m-%Y')}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DateSelectorApp()
    window.show()
    sys.exit(app.exec())