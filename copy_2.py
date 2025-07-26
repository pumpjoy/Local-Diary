import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QSizePolicy, 
    QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout,
    QScrollArea
)
from PyQt6.QtCore import Qt, QSize, QRect
import datetime

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Diary")

        self.minimum_window_size = QSize(800, 600)
        self.setGeometry(100, 100, 1024, 768)
        self.setMinimumSize(self.minimum_window_size)

        self.cal_month_num_rows = 6
        self.cal_month_num_cols = 7 
        self.cal_month_day_height = 30 
        self.cal_month_date_height = 300 

        self._create_widgets()
        self._setup_layouts()
        self._connect_signals()

    def _create_widgets(self):
        """Creates and initializes all the individual UI widgets."""
        # --- Widgets for Horizontal Layout 1 (Header Month) ---
        self.label_date = QLabel("DD MM YYYY")
        self.label_date.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.label_date.setContentsMargins(0,0,0,0)
        self.label_date.setWordWrap(True)

        self.bt_month_last = QPushButton("<")
        self.bt_today = QPushButton("Today")
        self.bt_month_next = QPushButton(">")

    def _setup_layouts(self):
        """Arranges widgets within their respective layouts."""

        # --- Horizontal Layout 1: Header Month ---
        layout_h_month = QHBoxLayout()
        layout_h_month.addWidget(self.bt_month_last)
        layout_h_month.addWidget(self.bt_today)
        layout_h_month.addWidget(self.bt_month_next)
        layout_h_month.setContentsMargins(0,0,0,14) # left, top, right, bottom
        layout_h_month.addStretch(1) 

        layout_h_day_header = QHBoxLayout()
        layout_h_day_header.addWidget(self.label_date, 1)  
        layout_h_day_header.addLayout(layout_h_month) 
        layout_h_day_header.setAlignment(layout_h_month, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # --- Calendar Month ---
        # Generate directly with main_vertical_layout 
        # to get the visuals I want 

        view_content_calendar_month = QVBoxLayout() 
        view_content_calendar_month.setContentsMargins(36, 14, 36, 14)
        view_content_calendar_month.setSpacing(0)
         
        view_content_calendar_month.addLayout(layout_h_day_header) 

        for row in range(self.cal_month_num_rows):
            layout_h_dates = QHBoxLayout()
            layout_h_dates.setContentsMargins(0, 0, 0, 0)
            layout_h_dates.setSpacing(0)

            current_row_fixed_height = 0
            background_color = ""
            border_style = ""
            text_prefix = ""
            if row == 0:
                current_row_fixed_height = self.cal_month_day_height
                background_color = "lightgreen"
                border_style = "1px solid darkgreen"
                text_prefix = "Days"
            else:
                current_row_fixed_height = self.cal_month_date_height
                background_color = "lightgray"
                border_style = "1px solid gray"
                text_prefix = "Date"


            # Generate for columns
            for col in range(self.cal_month_num_cols):
                if row == 0:
                    cell_widget = QLabel(f"{text_prefix} {col + 1}") # TODO: Change to Monday-Sunday
                    cell_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                else: 
                    cell_widget = QPushButton(f"{text_prefix} {row}-{col}")
 

                cell_widget.setStyleSheet(f"""
                    QWidget {{ /* QWidget applies to QLabel/QPushButton as they inherit from QWidget */
                        background-color: {background_color};
                        border: {border_style};
                    }}
                """)

                # Conditionally set fixed height
                if current_row_fixed_height > 0:
                    cell_widget.setFixedHeight(current_row_fixed_height)
                else:
                    # If no fixed height, let it expand vertically if needed
                    cell_widget.setSizePolicy(
                        QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
                    )

                layout_h_dates.addWidget(cell_widget, 1) # Add widget with stretch to fill horizontal space

            view_content_calendar_month.addLayout(layout_h_dates)
        view_content_calendar_month.addStretch(1)

        # Allow Calendar Month view to be scrollable
        view_calendar_month_scroll = QWidget()
        view_calendar_month_scroll.setLayout(layout_h_dates)
        self.grid_scroll_area = QScrollArea()
        self.grid_scroll_area.setWidgetResizable(True)
        self.grid_scroll_area.setWidget(view_calendar_month_scroll)
        self.grid_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.grid_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        

        self.setLayout(view_content_calendar_month)


    def _connect_signals(self):
        """Connects signals of widgets to their respective slots (methods)."""
        self.bt_month_last.clicked.connect(lambda: print("Button One Clicked!"))
        self.bt_today.clicked.connect(self._on_bt_today_clicked)
        self.bt_month_next.clicked.connect(lambda: print("Button Three Clicked!"))
 
    def _on_bt_today_clicked(self):
        """Updates the main label with the current time."""
        current_time = datetime.datetime.now()
        new_text = f"Updated: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        self.label_date.setText(new_text)
        print(f"Main label updated to: {new_text}")

    def _on_go_button_clicked(self):
        """Prints the text from the QLineEdit."""
        text_from_line_edit = self.line_edit.text()
        print(f"Go! button clicked. Line Edit contains: '{text_from_line_edit}'")


# --- Application Entry Point ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    # Dynamically set initial text after window creation
    today = datetime.date.today() # Get today's actual date
    window.label_date.setText(f"Welcome! Today is: {today.strftime('%d %B %Y')}")
    print(f"Main label initially set from __main__ to: {window.label_date.text()}")


    sys.exit(app.exec())