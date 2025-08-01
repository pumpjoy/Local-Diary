# TODO: Light theme on check box of settings are not dark pixels
# Will not do that because I will never use light theme.
# Test


import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QSizePolicy, 
    QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout,
    QScrollArea
)
from PyQt6.QtCore import Qt, QSize

import datetime
from dateutil.relativedelta import relativedelta


from helper.utils import *
from helper.config_manager import UserConfiguration
from helper.diary_property_manager import DiaryPropertyConfiguration

from view_setting import SettingsPageWidget

from asset.css_cheatsheet import (
    GLOBAL_DARK_QSS, GLOBAL_LIGHT_QSS,
    MAIN_LABEL_DARK_QSS, MAIN_LABEL_LIGHT_QSS, 
    MAIN_CALENDAR_DAY_CELL_LIGHT, MAIN_CALENDAR_DAY_CELL_DARK,
    MAIN_CALENDAR_TODAY_CELL_LIGHT, MAIN_CALENDAR_TODAY_CELL_DARK,
    MAIN_CALENDAR_DATE_NOT_THIS_MONTH_LIGHT, MAIN_CALENDAR_DATE_NOT_THIS_MONTH_DARK,
)
from asset.custom_cal_cell import CalendarCellWidget, CalendarHeaderWidget
from view_custom_property import CustomPropertyWidget
from view_custom_property_view import CustomPropertyViewWidget

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Diary")
        self.minimum_window_size = QSize(800, 600)
        self.setGeometry(100, 100, 1024, 768)
        self.setMinimumSize(self.minimum_window_size)

        # Load the configuration managers
        self.app_config = UserConfiguration(
            organization_name="TestOrg",
            application_name="Local_Diary"
        )

        self.diary_config = DiaryPropertyConfiguration()

        # Apply initial window size from config
        initial_window_size = self.app_config.get_setting('appearance.window_size', [800, 600])
        self.resize(initial_window_size[0], initial_window_size[1])

        # --- QStackedWidget --- 
        self.main_page_widget = None
        self.settings_page_widget = None
        self.custom_property_page_widget = None
        self.custom_property_page_view_widget = None
        self.main_page_index = 0
        self.settings_page_index = 1
        self.custom_diary_property_index = 2 # Customize one's diary template
        self.custom_diary_view = 3 # Calendar view's CustomCellWidget visually see what properties
        self.stacked_widget = None # Initialized in _setup_layouts

        # --- Calendar month settings ---
        self.cal_month_num_rows = 6
        self.cal_month_num_cols = 7 
        self.cal_month_day_height = 28 
        self.cal_month_date_min_height = 100

        self.first_day_is_monday = False

        self._create_widgets()
        self._setup_layouts()
        self._connect_signals()
        self._update_ui_theme()
        self._update_calendar_cells()

    def _create_widgets(self): 
        pass


    def _setup_layouts(self):
        """Arranges widgets within their respective layouts."""
        # --- Stacked Widget ---
        
        self.main_page_widget = self._create_main_page_widget()
        self.settings_page_widget = SettingsPageWidget(self.app_config)
        self.custom_property_page_widget = CustomPropertyWidget(self.app_config, self.diary_config) # 2 modes, either customize or view mode (reusing it)
        self.custom_property_page_view_widget = CustomPropertyViewWidget()
        
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.stacked_widget.addWidget(self.main_page_widget)
        self.stacked_widget.addWidget(self.settings_page_widget)
        self.stacked_widget.addWidget(self.custom_property_page_widget)
        self.stacked_widget.addWidget(self.custom_property_page_view_widget)
        

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)  
    

    # --- Signal Connections ---
    def _connect_signals(self):
        """Connects signals of widgets to their respective slots (methods)."""
        # --- Setting related signals ---
        self.bt_setting.clicked.connect(self._show_settings_page)
        # Connect signals from the separate SettingsPageWidget instance
        self.settings_page_widget.back_to_main_requested.connect(self._show_main_page)
        self.settings_page_widget.settings_saved.connect(self._handle_settings_saved_from_settings_page)

        # --- Custom Property related signals --- 
        self.bt_custom_property.clicked.connect(self._show_custom_property_page)
        # Connect signals from the separate SettingsPageWidget instance
        self.custom_property_page_widget.back_to_main_requested.connect(self._show_main_page) 


        # --- Local - Calendar month navigation signals ---
        self.bt_month_last.clicked.connect(lambda: self._update_calendar_cells(mode="prev"))
        self.bt_today.clicked.connect(lambda: self._update_calendar_cells(mode="today"))
        self.bt_month_next.clicked.connect(lambda: self._update_calendar_cells(mode="next"))
    
    # --- Main Page Logic ---
    def _create_main_page_widget(self):
        """
        Creates and initializes all the individual UI widgets.
        @return: QWidget containing the main page layout with calendar and settings button.
        """
        # Mixed _setup_ui and _create_widgets from before
        
        self.bt_setting = QPushButton("\u22EE")
        self.bt_setting.setFixedSize(30, 30)
        self.bt_setting.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # --- Widgets for Horizontal Layout 1 (Header Month) ---
        this_date = self.app_config.get_setting('current_month', datetime.datetime.now())
        this_date = datetime.datetime.fromisoformat(this_date)  
        self.main_label = QLabel(this_date.strftime('%B %Y'))
        
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.main_label.setContentsMargins(0,0,0,0)
        self.main_label.setWordWrap(True)

        self.bt_month_last = QPushButton("<")
        self.bt_month_last.setFixedSize(30, 30)
        self.bt_month_last.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.bt_today = QPushButton("Today")
        self.bt_today.setFixedSize(80, 30)
        self.bt_today.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.bt_month_next = QPushButton(">")
        self.bt_month_next.setFixedSize(30, 30)
        self.bt_month_next.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # --- Horizontal Layout 1: Header Month ---
        row_h_month_control = QHBoxLayout()
        row_h_month_control.addWidget(self.bt_month_last)
        row_h_month_control.addWidget(self.bt_today)
        row_h_month_control.addWidget(self.bt_month_next)
        row_h_month_control.setContentsMargins(14,0,0,0) 
        row_h_month_control.addStretch(1) 

        row_h_mon = QHBoxLayout()
        row_h_mon.addWidget(self.main_label, 1)  
        row_h_mon.addLayout(row_h_month_control) 
        row_h_mon.setAlignment(row_h_month_control, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # --- Widgets for Horizontal Layout 2 (Custom Diary Property) ---

        self.bt_custom_property = QPushButton("Customize \nProperty")
        self.bt_custom_property.setFixedSize(80, 40)
        self.bt_custom_property.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        row_h_custom_property = QHBoxLayout()
        row_h_custom_property.addWidget(self.bt_custom_property)
        row_h_custom_property.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # --- Calendar Month ---
        # Generate directly with main_vertical_layout 
        # to get the visuals I want 

        self.first_day_is_monday = not self.app_config.get_setting('settings_page.first_day_is_sunday', True)

        view_content_calendar_month = QVBoxLayout() 
        view_content_calendar_month.setContentsMargins(0, 0, 0, 0)
        view_content_calendar_month.setSpacing(0)
        
        # Initiate a list to hold references to calendar widgets
        self.calendar_widgets_reference = {}
        for row in range(self.cal_month_num_rows):
            layout_h_dates = QHBoxLayout()
            layout_h_dates.setContentsMargins(0, 0, 0, 0)
            layout_h_dates.setSpacing(0)


            # Generate for columns 
            if self.first_day_is_monday:
                days = DAY_OF_WEEK[:]  
            else: 
                days = DAY_OF_WEEK[-1:] + DAY_OF_WEEK[:-1]  # Sunday first 

             
            this_month = generate_month_dates(this_date, self.first_day_is_monday) # Get current month  
            current_theme = self.app_config.get_setting('appearance.theme', 'dark')
            
            for col in range(self.cal_month_num_cols):
                if row == 0:
                    # Day header cells
                    cell_widget = CalendarHeaderWidget(f"{days[col]}") 
                else:  
                    # Date cells
                    cell_widget = CalendarCellWidget(f"{this_month[(row - 1) * self.cal_month_num_cols + col].day}") 
                
                self.calendar_widgets_reference[(row, col)] = cell_widget  # Store reference for later use

                combined_style = (
                    (MAIN_CALENDAR_DAY_CELL_LIGHT if current_theme == 'light' else MAIN_CALENDAR_DAY_CELL_DARK) 
                )
                cell_widget.setStyleSheet(combined_style)

                if row == 0: 
                    cell_widget.setFixedHeight(self.cal_month_day_height)
                else:
                    cell_widget.setMinimumHeight(self.cal_month_date_min_height)
                    cell_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
                
                
                layout_h_dates.addWidget(cell_widget, 1)

            view_content_calendar_month.addLayout(layout_h_dates)
        view_content_calendar_month.addStretch(1)

        # Allow Calendar Month view to be scrollable
        view_scroll_calendar_month = QWidget()
        view_scroll_calendar_month.setLayout(view_content_calendar_month)
        grid_scroll_area = QScrollArea()
        grid_scroll_area.setWidgetResizable(True)
        grid_scroll_area.setWidget(view_scroll_calendar_month)
        grid_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        grid_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # --- Main Window View ---
        main_window = QWidget()
        main_window_view = QVBoxLayout(main_window)
        main_window_view.setContentsMargins(14, 14, 14, 36) # left, top, right, bottom
        main_window_view.addWidget(self.bt_setting, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        main_window_view.addLayout(row_h_mon) 
        main_window_view.addLayout(row_h_custom_property)
        main_window_view.addSpacing(5)
        main_window_view.addWidget(grid_scroll_area, 1)
        
        # self.setLayout(main_window_view)
        return main_window


    # --- Page Navigation Methods ---
    def _show_main_page(self):
        """Switches the QStackedWidget to display the main application page."""
        # When switching from settings to main, ensure main page UI elements are updated
        self._update_ui_theme()
        self.stacked_widget.setCurrentIndex(self.main_page_index)
        self.setWindowTitle("Dynamic Cell Content & Settings Page")
 
    def _show_settings_page(self):
        """Switches the QStackedWidget to display the settings page."""
        # Tell settings page to load fresh data from config before showing it
        self.settings_page_widget.load_settings_into_ui()
        self._update_ui_theme()
        self.stacked_widget.setCurrentIndex(self.settings_page_index)
        self.setWindowTitle("Application Settings")

    def _show_custom_property_page(self):
        """Switches the QStackedWidget to display the custom property page."""
        # Tell custom property page to load fresh data from config before showing it
        self.custom_property_page_widget.load_into_ui
        self.stacked_widget.setCurrentIndex(self.custom_diary_property_index)
        self.setWindowTitle("Custom Property Settings")

    # --- Methods to react to settings changes ---
    def _handle_settings_saved_from_settings_page(self):
        """
        Slot to react to the settings_saved signal from SettingsPageWidget.
        Use this to update any main_view UI elements that depend on settings.
        """
        print("Main view received settings_saved signal. Updating UI.")
        self._update_ui_theme() 
        self._update_calendar_cells()
    
    # --- Other Application Logic --- 
    
    def _on_bt_today_clicked(self):
        """Updates the main label with the current time."""
        current_time = datetime.datetime.now().date()
        new_text = f" {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        self.main_label.setText(new_text)
        print(f"Main label updated to: {new_text}") 

    def closeEvent(self, event):
        """
        Overrides the close event to save application state before exiting.
        """
        self.app_config.set_setting('appearance.window_size', [self.width(), self.height()])
        self.app_config.save_config()
        super().closeEvent(event)

    
    def _update_ui_theme(self):
        """
        Applies the current theme settings to the entire application and specific widgets.
        Called on startup and when settings are saved.
        """
        current_theme = self.app_config.get_setting('appearance.theme', 'dark')
        print(f"Applying theme: {current_theme}")

        # Apply global stylesheet to the QApplication instance
        QApplication.instance().setStyleSheet(
            GLOBAL_DARK_QSS if current_theme == 'dark' else GLOBAL_LIGHT_QSS
        )

        # Update main page header label 
        self.main_label.setStyleSheet(MAIN_LABEL_DARK_QSS if current_theme == 'dark' else MAIN_LABEL_LIGHT_QSS) 
        self.settings_page_widget.update_theme_style(current_theme)
        self.custom_property_page_widget.update_theme_style(current_theme)

        

    def _update_calendar_cells(self, mode="None"):
        """
        Updates the calendar cell labels based on the current first day setting.
        """
        self.first_day_is_monday = not self.app_config.get_setting('settings_page.first_day_is_sunday', True)
        today = datetime.datetime.now().date()
        
        # mode = prev, today, next
        
        this_date = self.app_config.get_setting('current_month', datetime.datetime.now())
        this_date = datetime.datetime.fromisoformat(this_date) 
        
        if mode == "prev":
            this_date = this_date - relativedelta(months=1)  
        elif mode == "today":
            this_date = datetime.datetime.now().date()
        elif mode == "next":
            this_date = this_date + relativedelta(months=1)
         
        self.main_label.setText(this_date.strftime('%B %Y'))
        self.app_config.set_setting('current_month', this_date.isoformat()) 
        this_month = generate_month_dates(this_date, self.first_day_is_monday)

        # Update day header cells (row 0)
        if self.first_day_is_monday:
            days = DAY_OF_WEEK[:]
        else:
            days = DAY_OF_WEEK[-1:] + DAY_OF_WEEK[:-1]

        for col in range(self.cal_month_num_cols):
            cell_widget = self.calendar_widgets_reference.get((0, col))
            if cell_widget: 
                cell_widget.cus_set_text(days[col])

        # Update date cells (rows 1+)
        for row in range(1, self.cal_month_num_rows):
            for col in range(self.cal_month_num_cols):
                cell_widget = self.calendar_widgets_reference.get((row, col))
                idx = (row - 1) * self.cal_month_num_cols + col
                if cell_widget and idx < len(this_month):
                    cell_date = this_month[idx] 
                    
                    current_theme = self.app_config.get_setting('appearance.theme', 'dark') 
                    style = MAIN_CALENDAR_DAY_CELL_LIGHT if current_theme == 'light' else MAIN_CALENDAR_DAY_CELL_DARK      

                    cell_widget.cus_set_text(str(cell_date.day))
                    cell_widget.setStyleSheet(style)

                    # Check if this cell is within the current month
                    if cell_date.month != this_date.month: 
                        cell_widget.setStyleSheet(MAIN_CALENDAR_DATE_NOT_THIS_MONTH_LIGHT if current_theme == "light" else MAIN_CALENDAR_DATE_NOT_THIS_MONTH_DARK) 
                    
                    # Check if this cell is today, highlight if yes
                    if cell_date == today: 
                        if hasattr(cell_widget, "set_today"):
                            cell_widget.set_today(True)   
                            cell_widget.setStyleSheet(MAIN_CALENDAR_TODAY_CELL_LIGHT if current_theme == "light" else MAIN_CALENDAR_TODAY_CELL_DARK )
                    else:
                        if hasattr(cell_widget, "set_today"):
                            cell_widget.set_today(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())