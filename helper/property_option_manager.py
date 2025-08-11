import datetime
import json
import os
from PyQt6.QtCore import QStandardPaths, QDir

class PropertyOptionManager:
    """
    For managing property_value of m/select/status property types
    Each PropertyOptionManager only holds a single property_id + property_type 
    """

    def __init__(self, property_id, property_type, organization_name="TestOrg", application_name="Local_Diary",):
        
        self.organization_name = organization_name
        self.application_name = application_name

        self.property_id = property_id
        self.property_type = property_type

        self.property_dir = self._get_config_directory()
        self.property_file_path = os.path.join(self.property_dir, "property_option.json")
        self.property_data = {}
 
        self._ensure_config_directory_exists()
        self.load_option_file()


    def _get_config_directory(self):
        """
        Determines the standard, platform-specific directory for application configuration files.
        On Windows: C:/Users/<User>/AppData/Roaming/Company/AppName/
        On macOS: /Users/<User>/Library/Application Support/Company/AppName/
        On Linux: /home/<User>/.config/Company/AppName/
        """
        config_location = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppConfigLocation # Best for app-specific data
        )
        if not config_location:
            # Fallback if QStandardPaths doesn't return a path (rare)
            config_location = os.path.join(
                QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation),
                f".{self.organization_name}",
                self.application_name
            )
        return config_location

    def _ensure_config_directory_exists(self):
        """
        Creates the configuration directory if it doesn't already exist.
        """
        if not QDir().mkpath(self.property_dir):
            print(f"Warning: Could not create config directory: {self.property_dir}")

    # --- Actual tasks ---
    def load_option_file(self):
        """
        Loads the whole file that contains data for property_option_manager. 
        If file doesn't exist or is corrupted, prints Error Message.
        """
        if os.path.exists(self.property_file_path):
            try:
                with open(self.property_file_path, 'r', encoding='utf-8') as f:
                    self.property_data = json.load(f)
                print(f"Configuration loaded from: {self.property_file_path}")
            except json.JSONDecodeError as e:
                # Handle cases where the JSON file is malformed
                print(f"Error loading config file (JSON decode error): {e}")
                print("Initializing with default settings.")
                self.property_data = self._get_default_config()
            except Exception as e:
                # Handle other potential file I/O errors (e.g., permission issues)
                print(f"Error loading config file: {e}")
                print("Initializing with default settings.")
                self.property_data = self._get_default_config()
        else:
            # File doesn't exist, so initialize with defaults
            print(f"Config file not found: {self.property_file_path}.")

    def get_property_option(self, property_id: int, property_type: str):
        """
        Loads the chunk of information on a specific option
        based on property_id and property_type.
        If none matched property_id and property_type,
        return an error dialog to not run this app at all.
        """
        for prop_dict in self.property_data:
            # Check if both the ID and type match
            if prop_dict['property_id'] == property_id and prop_dict['property_type'] == property_type:
                return prop_dict['property_value']
        
        return None # TODO: Give QMessageBox warning

    def set_property_option_value(self, property_id: int, property_type:str):
        """Changes/adds to the value of the property based on id and type"""
        pass

    # --- Set new property option ---
    def set_new_property(self, property_id: int, property_key:str, property_type:str): 
        """
        Add new m/select/status is pressed
        Creates empty property_value
        """
        pass