from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QColor, QFontMetrics
from PyQt6.QtCore import Qt, QPoint, QRect # QRect is useful for geometry calculations

class CalendarCellWidget(QWidget): # <--- IMPORTANT: Inherit from QWidget, not QVBoxLayout
    def __init__(self, text="", is_today=False, *args, **kwargs):
        super().__init__(*args, **kwargs) # Call the QWidget's constructor

        self.is_today = is_today
        self.margin = 8 # Margin for content inside the cell

        # 1. Create the QVBoxLayout instance
        # This layout will manage the arrangement of widgets *inside* this CalendarCellWidget
        self.main_layout = QVBoxLayout(self) # Pass 'self' (this QWidget) as the parent for the layout
                                            # This automatically sets the layout for this widget.

        # 2. Configure the layout's margins and spacing
        # These margins are between the CalendarCellWidget's border and its content
        self.main_layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        self.main_layout.setSpacing(0) # No spacing between items within this cell (e.g., number and event dot)

        # 3. Create the QLabel to display the number/text
        self.number_label = QLabel(text)
        self.number_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # Optional: Apply some default styling to the label itself
        font = self.number_label.font()
        font.setBold(True)
        self.number_label.setFont(font)
        # self.number_label.setStyleSheet("color: black;") # Example: ensure text color

        # 4. Add the QLabel to the QVBoxLayout
        self.main_layout.addWidget(self.number_label)

        # Optional: Add a stretch to push the number_label to the top
        # This ensures the number stays at the top-left if the cell is larger
        self.main_layout.addStretch() 

        # 5. Set a fixed size for the CalendarCellWidget itself
        # This is important for it to behave like a consistent cell in a grid
        self.setFixedSize(70, 70) # Adjust size as needed for your calendar layout

    def set_today(self, is_today):
        """Sets whether this cell represents today's date and triggers a repaint."""
        if self.is_today != is_today: # Only update if state changes
            self.is_today = is_today
            self.update() # Request a repaint to draw/remove the circle

    def setText(self, text):
        """Sets the text displayed in the cell's number label."""
        if self.number_label.text() != text: # Only update if text changes
            self.number_label.setText(text)
            self.update() # Request a repaint (especially if text metrics affect circle drawing)

    def paintEvent(self, event):
        """Custom painting for the 'today' circle."""
        super().paintEvent(event) # IMPORTANT: Call the parent QWidget's paintEvent first
                                  # This ensures the background, borders, etc., are drawn.

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.is_today:
            # Re-calculate text position and bounding box for precise circle drawing
            # This logic assumes the text is drawn at the top-left within the content margins
            font = self.font() # Use the cell's font (which can be set for the widget)
            metrics = QFontMetrics(font)
            display_text = self.number_label.text() # Get the current text from the internal QLabel

            # Calculate text position relative to this widget's content margin
            # The QLabel's actual painted position might differ slightly based on its alignment
            # but for the custom circle, we'll draw it based on a consistent calculation.
            text_x = self.main_layout.contentsMargins().left()
            text_y = self.main_layout.contentsMargins().top() + metrics.ascent()

            # Calculate the bounding rect of the text if it were drawn directly by the painter
            text_rect = metrics.boundingRect(display_text)
            text_rect.moveTopLeft(QPoint(text_x, self.main_layout.contentsMargins().top()))

            # Calculate circle center and radius based on the text_rect
            center_x = text_rect.left() + text_rect.width() // 2 + 1
            center_y = text_rect.top() + text_rect.height() // 2 + 1
            radius = max(text_rect.width(), text_rect.height()) // 2 + 6

            pen = QPen(QColor("red"), 2)
            painter.setPen(pen)
            painter.drawEllipse(QPoint(center_x, center_y), radius, radius)

# Example usage (same as before, showing it works as a cell in a grid)
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
    import sys
    import datetime

    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("CalendarCellWidget as QWidget with QVBoxLayout")
            self.setGeometry(100, 100, 500, 500) # x, y, width, height

            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            grid_layout = QGridLayout(central_widget)
            grid_layout.setSpacing(2) # Spacing between CalendarCellWidgets

            # Get current date for 'today' highlighting
            today = datetime.date.today()
            
            # Create and add CalendarCellWidgets to the grid
            # This simulates a small calendar month
            day_counter = 1
            for row in range(6): # 6 rows for a typical month grid (including header)
                for col in range(7): # 7 columns for days of the week
                    if row == 0:
                        # Day headers
                        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                        cell = CalendarCellWidget(text=days_of_week[col])
                        cell.number_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center header text
                        # cell.number_label.setFont(QApplication.font().pointSize())
                        cell.number_label.setStyleSheet("font-weight: bold; color: #555;")
                        cell.setStyleSheet("background-color: #f0f0f0;") # Light background for headers
                    else:
                        # Date cells
                        if day_counter <= 31: # Example: up to 31 days
                            current_date_for_cell = datetime.date(today.year, today.month, day_counter)
                            is_today_cell = (current_date_for_cell == today)
                            cell = CalendarCellWidget(text=str(day_counter), is_today=is_today_cell)
                            
                            # Apply general cell background
                            cell.setStyleSheet("background-color: white; border: 1px solid #eee;")

                            # Example: gray out days not in the current month (mocking for simplicity)
                            if day_counter > 25: # Just an example condition
                                cell.number_label.setStyleSheet("color: lightgrey;")
                            else:
                                cell.number_label.setStyleSheet("color: black;") # Ensure color for current month days

                            day_counter += 1
                        else:
                            # Empty cells after the month ends
                            cell = CalendarCellWidget(text="")
                            cell.setStyleSheet("background-color: #f8f8f8;") # Lighter background for empty cells

                    grid_layout.addWidget(cell, row, col)

    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())