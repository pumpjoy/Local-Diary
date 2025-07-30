# css_cheatsheet.py

# --- Global Constants ---
GLOBAL_DARK_BACKGROUND = 1
GLOBAL_CAL_CELL_FONT_SIZE = 14


# --- Global Application Stylesheets ---
# These apply to QApplication.instance()
GLOBAL_LIGHT_QSS = """
    QWidget {
        background-color: #F0F0F0;
        color: #333333;
        font-family: Arial, sans-serif;
    }
    QPushButton {
        background-color: #E0E0E0;
        border: 1px solid #B0B0B0;
        padding: 5px 10px;
        border-radius: 3px;
        color: #333333;
    }
    QPushButton:hover {
        background-color: #D0D0D0;
    } 
    QScrollArea {
        border: 1px solid #D0D0D0;
        background-color: white; /* Scroll area content background */
    } 
"""

GLOBAL_DARK_QSS = """
    QWidget {
        background-color: #2E2E2E;
        color: #E0E0E0;
        font-family: Arial, sans-serif;
    }
    QPushButton {
        background-color: #555555;
        border: 1px solid #777777;
        color: white;
        padding: 5px 10px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #666666;
    } 
    QScrollArea {
        border: 1px solid #444444;
        background-color: #383838; /* Scroll area content background */
    } 
"""

# --- Main Page Specific Styles ---
# Styles for the main header label (QLabel)
MAIN_HEADER_LIGHT_QSS = "background-color: lightgray; color: black; font-weight: bold; padding: 2px; font-size: 14px;"
MAIN_HEADER_DARK_QSS = "background-color: #444444; color: white; font-weight: bold; padding: 2px; font-size: 14px;"

# Styles for main page Calendar 
MAIN_CALENDAR_DAY_CELL_LIGHT = f"""
QWidget {{ 
    background-color: lightgray; 
    border: 1px solid darkgray; 
    color: black;  
    font-size: {GLOBAL_CAL_CELL_FONT_SIZE}px;
    }} 
"""
MAIN_CALENDAR_DAY_CELL_DARK = f"""
QWidget {{ 
    background-color: #333333; 
    border: 1px solid #555555; 
    color: white; 
    font-size: {GLOBAL_CAL_CELL_FONT_SIZE}px;
    }} 
""" 

MAIN_CALENDAR_TODAY_CELL_LIGHT = f"""
QWidget {{ 
    background-color: lightgray; 
    border: 1px solid red; 
    color: red;  
    font-size: {GLOBAL_CAL_CELL_FONT_SIZE}px;
    }}
"""
MAIN_CALENDAR_TODAY_CELL_DARK = f"""
QWidget {{ 
    background-color: #333333; 
    border: 1px solid yellow; 
    color: yellow; 
    font-size: {GLOBAL_CAL_CELL_FONT_SIZE}px;
    }}
""" 

 

MAIN_CALENDAR_DATE_NOT_THIS_MONTH_LIGHT = f"""
QWidget {{ 
    background-color: lightgray; 
    border: 1px solid darkgray; 
    color: gray; 
    font-size: {GLOBAL_CAL_CELL_FONT_SIZE}px;
    }}
"""

MAIN_CALENDAR_DATE_NOT_THIS_MONTH_DARK  = f"""
QWidget {{ 
    background-color: #333333; 
    border: 1px solid #555555; 
    color: gray; 
    font-size: {GLOBAL_CAL_CELL_FONT_SIZE}px;
    }}
"""


# --- Settings Page Specific Styles ---
# Styles for the SettingsPageWidget's root QWidget
SETTINGS_PAGE_LIGHT_QSS = """
    QWidget {
        background-color: #F0F0F0; /* Override global background if needed */
        color: #333333;
    }
    QLabel { /* Labels within SettingsPageWidget */
        color: #333333;
    }
"""

SETTINGS_PAGE_DARK_QSS = """
    QWidget {
        background-color: #333333; /* Override global background if needed */
        color: #E0E0E0;
    }
    QLabel { /* Labels within SettingsPageWidget */
        color: #E0E0E0;
    }
"""

# Styles for the SettingsPageWidget's header label
SETTINGS_HEADER_LIGHT_QSS = "background-color: #ADD8E6; color: black; font-weight: bold; padding: 5px;"
SETTINGS_HEADER_DARK_QSS = "background-color: #555555; color: white; font-weight: bold; padding: 5px;"


# Styles for QLineEdit within SettingsPageWidget
SETTINGS_LINE_EDIT_LIGHT_QSS = "QLineEdit { background-color: white; color: black; border: 1px solid #AAA; }"
SETTINGS_LINE_EDIT_DARK_QSS = "QLineEdit { background-color: #444444; color: #E0E0E0; border: 1px solid #666; }"