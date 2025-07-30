import sys
import json

from PyQt6.QtWidgets import QApplication

from temp_archive.view_main import MyWindow


 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())