# css_cheatsheet.py

# Borrowing this place to put types_of_properties 
TYPES_OF_PROPERTIES = [
    "text", "number", "select", "multi_select", "status", "checkbox",
    ]

PROPERTY_OPTIONS_COLOUR = [
    "red", "blue", "green", "yellow"
]
PROPERTY_OPTIONS_COLOUR_HEX = [
    "#FF8C00", "#ADD8E6", "#90EE90", "#FFFF00"
]


# Future can have  
# created_by, last_modified_by,
# created_time,  last_modified_time,
# location, last_modified_at, created_at, 
# tags, etc for easier creation of custom properties <- waaaay too much work for now

# --- Global Constants --- 
WINDOW_MARGIN = (14, 14, 14, 36) # left, top, right, bottom 

# Main header label (QLabel)
MAIN_LABEL_FONT_SIZE = 14
MAIN_LABEL_MARGIN = 10
MAIN_LABEL_LIGHT_QSS = f"background-color: lightgray; color: black; font-weight: bold; font-size: {MAIN_LABEL_FONT_SIZE}pt;"
MAIN_LABEL_DARK_QSS = f"background-color: #444444; color: white; font-weight: bold; font-size: {MAIN_LABEL_FONT_SIZE}pt;"

BT_BACK_TO_MAIN_SIZE = (100, 30)

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
        border: 1pt solid #B0B0B0;
        padding: 5pt 10pt;
        border-radius: 3pt;
        color: #333333;
    }
    QPushButton:hover {
        background-color: #D0D0D0;
    } 
    QScrollArea {
        border: 1pt solid #D0D0D0;
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
        border: 1pt solid #777777;
        color: white;
        padding: 5pt 10pt;
        border-radius: 3pt;
    }
    QPushButton:hover {
        background-color: #666666;
    } 
    QScrollArea {
        border: 1pt solid #444444;
        background-color: #383838; /* Scroll area content background */
    } 
"""

# --- Main Page Specific Styles ---
### Constants

MAIN_PAGE_CAL_CELL_FONT_SIZE = 11
MAIN_PAGE_CAL_HEAD_MARGIN = 4


### Styles
### Calendar Cell 
MAIN_CALENDAR_CELL_BORDER = 1
MAIN_CALENDAR_DAY_LIGHT = f"""
QWidget {{ 
    background-color: lightgray; 
    border: {MAIN_CALENDAR_CELL_BORDER}px solid darkgray; 
    color: black;  
    font-size: {MAIN_PAGE_CAL_CELL_FONT_SIZE}pt;
    }} 
"""
MAIN_CALENDAR_DAY_DARK = f"""
QWidget {{ 
    background-color: #333333; 
    border: {MAIN_CALENDAR_CELL_BORDER}px solid #555555; 
    color: white; 
    font-size: {MAIN_PAGE_CAL_CELL_FONT_SIZE}pt;
    }} 
""" 
MAIN_CALENDAR_TODAY_LIGHT = f"""
QWidget {{ 
    background-color: lightgray; 
    border: {MAIN_CALENDAR_CELL_BORDER}px solid red; 
    color: red;  
    font-size: {MAIN_PAGE_CAL_CELL_FONT_SIZE}pt;
    }}
"""
MAIN_CALENDAR_TODAY_DARK = f"""
QWidget {{ 
    background-color: #333333; 
    border: {MAIN_CALENDAR_CELL_BORDER}px solid yellow; 
    color: yellow; 
    font-size: {MAIN_PAGE_CAL_CELL_FONT_SIZE}pt;
    }}
""" 
MAIN_CALENDAR_DATE_NOT_THIS_MONTH_LIGHT = f"""
QWidget {{ 
    background-color: lightgray; 
    border: {MAIN_CALENDAR_CELL_BORDER}px solid darkgray; 
    color: gray; 
    font-size: {MAIN_PAGE_CAL_CELL_FONT_SIZE}pt;
    }}
"""
MAIN_CALENDAR_DATE_NOT_THIS_MONTH_DARK  = f"""
QWidget {{ 
    background-color: #333333; 
    border: {MAIN_CALENDAR_CELL_BORDER}px solid #555555; 
    color: gray; 
    font-size: {MAIN_PAGE_CAL_CELL_FONT_SIZE}pt;
    }}
"""

# --- Settings Page Specific Styles ---
 

# ------------------------------------------
# Class definition
# Makes import not as disgusting


class MAIN_PAGE_WIDGETS_SIZE:
    BT_SETTING = (30, 30)
    BT_CUSTOM_PROPERTY = (80, 40)
    BT_MONTH_LAST = (30, 30)
    BT_MONTH_TODAY = (80, 30)
    BT_MONTH_NEXT = (30, 30)

class MAIN_CALENDAR_CELL_CSS:
    DAY_LIGHT = MAIN_CALENDAR_DAY_LIGHT
    DAY_DARK = MAIN_CALENDAR_DAY_DARK
    TODAY_LIGHT = MAIN_CALENDAR_TODAY_LIGHT
    TODAY_DARK = MAIN_CALENDAR_TODAY_DARK
    NOT_THIS_MONTH_LIGHT = MAIN_CALENDAR_DATE_NOT_THIS_MONTH_LIGHT
    NOT_THIS_MONTH_DARK = MAIN_CALENDAR_DATE_NOT_THIS_MONTH_DARK