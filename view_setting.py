# settings_view.py
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit,
    QHBoxLayout, QVBoxLayout, QGridLayout, QCheckBox,
    QMenu
)
from PyQt6.QtGui import QAction

from asset.css_cheatsheet import (
    WINDOW_MARGIN,
    MAIN_LABEL_LIGHT_QSS, MAIN_LABEL_DARK_QSS, 
    BT_BACK_TO_MAIN_SIZE,
    GLOBAL_LIGHT_QSS, GLOBAL_DARK_QSS,
)


class SettingsPageWidget(QWidget):
    # Signals emitted by this widget for the parent to react to
    requested_back_to_main = pyqtSignal()
    settings_saved = pyqtSignal() # Emitted after settings are saved to config_manager

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager # Store reference to the config manager
        self._setup_ui()
        self._connect_signals()
        self.load_settings_into_ui() # Load initial settings when widget is created

    def _setup_ui(self):
        settings_page_v_layout = QVBoxLayout(self)
        settings_page_v_layout.setContentsMargins(*WINDOW_MARGIN)
        settings_page_v_layout.setSpacing(5)

        # Header section for the settings page
        settings_header_h_layout = QHBoxLayout()
        self.main_label = QLabel("Settings")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        current_theme = self.config_manager.get_setting('appearance.theme', 'dark')
        self.main_label.setStyleSheet(MAIN_LABEL_DARK_QSS if current_theme == 'dark' else MAIN_LABEL_LIGHT_QSS)
        self.bt_back_to_main = QPushButton("Back to Main")
        self.bt_back_to_main.setFixedSize(*BT_BACK_TO_MAIN_SIZE)
        settings_header_h_layout.addWidget(self.main_label, 1)
        settings_header_h_layout.addWidget(self.bt_back_to_main)

        # --- Content ---
        # Theme Setting
        self.theme_checkbox = QCheckBox("Use Light Mode") 

        # First day is Monday Setting
        self.first_day_is_sunday = QCheckBox("First day of week is Sunday")
        
        # Actual View
        settings_form_layout = QGridLayout()
        settings_form_layout.setContentsMargins(0, 0, 0, 0)
        settings_form_layout.setSpacing(10)
        settings_form_layout.addWidget(self.theme_checkbox, 0, 0)
        settings_form_layout.addWidget(self.first_day_is_sunday, 1, 0)
        

        settings_page_v_layout.addLayout(settings_header_h_layout)
        settings_page_v_layout.addSpacing(20)
        settings_page_v_layout.addLayout(settings_form_layout)
        settings_page_v_layout.addStretch(1) # Push content to the top

    def _connect_signals(self):
        """Connects signals specific to this settings page."""
        self.bt_back_to_main.clicked.connect(self._on_bt_back_to_main_clicked) 

    def _on_bt_back_to_main_clicked(self):
        self._save_settings_from_ui()
        self.requested_back_to_main.emit()

    def load_settings_into_ui(self):
        """Loads settings from the config manager into the UI widgets."""
        current_theme = self.config_manager.get_setting('appearance.theme', 'dark')
        self.theme_checkbox.setChecked(current_theme == 'light')
        self.first_day_is_sunday.setChecked(self.config_manager.get_setting('settings_page.first_day_is_sunday', True)) 

    def _save_settings_from_ui(self):
        """Reads settings from the UI widgets and saves them to the config manager."""
        new_theme = 'light' if self.theme_checkbox.isChecked() else 'dark'
        self.config_manager.set_setting('appearance.theme', new_theme)

        self.config_manager.set_setting('settings_page.first_day_is_sunday', self.first_day_is_sunday.isChecked()) 
        self.config_manager.save_config() # Persist changes to file
        print("Settings saved from SettingsPageWidget.")
        self.settings_saved.emit() # Notify parent that settings have been saved

    def update_theme_style(self, theme_name):
        """
        Updates the theme-dependent styles of this widget and its children.
        Called by the main window.
        """
        if theme_name == 'light':
            self.setStyleSheet(GLOBAL_LIGHT_QSS)
            self.main_label.setStyleSheet(MAIN_LABEL_LIGHT_QSS)  
        else: # dark theme
            self.setStyleSheet(GLOBAL_DARK_QSS) 
            self.main_label.setStyleSheet(MAIN_LABEL_DARK_QSS)  
