# Havent prepare the actual file saving

import datetime
import json
import os
from PyQt6.QtCore import QStandardPaths, QDir

class DiaryPropertyConfiguration:
    def __init__(self, organization_name="TestOrg", application_name="Local_Diary", edit_mode: bool=True, date=None):
        """
        Initializes the configuration manager.
        Sets up the path to the config file and loads existing settings or defaults.
        """
        self.organization_name = organization_name
        self.application_name = application_name 
        self.change_mode(edit_mode)

        self.config_data = {}
 
        self._ensure_config_directory_exists()
        self.load_config()

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
    
    def get_data_directory(self):
        """
        Gets the path to the 'data' subfolder within the config directory
        and ensures it exists.
        """
        config_dir = self._get_config_directory()
        data_dir = os.path.join(config_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return data_dir
    
    def change_mode(self, edit_mode: bool, date=None):
        """
        Changes the mode of the configuration manager.
        If edit_mode is True, it uses the config directory.
        If False, it uses the data directory with a specific date.
        """
        self.edit_mode = edit_mode
        if edit_mode:
            self.config_dir = self._get_config_directory()
            self.config_file_path = os.path.join(self.config_dir, "diary_property.json")
        else:
            if date is None:
                raise ValueError("Date must be set when not in edit mode.")
            self.config_dir = self.get_data_directory()
            self.config_file_path = os.path.join(self.config_dir, f"entry_{date}.json")
        
        self._ensure_config_directory_exists()
        return self.config_file_path


    def _ensure_config_directory_exists(self):
        """
        Creates the configuration directory if it doesn't already exist.
        """
        if not QDir().mkpath(self.config_dir):
            print(f"Warning: Could not create config directory: {self.config_dir}")

    def load_config(self):
        """
        Loads configuration data from the config file.
        If file doesn't exist or is corrupted, it initializes with default settings.
        """
        if os.path.exists(self.config_file_path):
            try:
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                print(f"Configuration loaded from: {self.config_file_path}")
            except json.JSONDecodeError as e:
                # Handle cases where the JSON file is malformed
                print(f"Error loading config file (JSON decode error): {e}")
                print("Initializing with default settings.")
                self.config_data = self._get_default_config()
            except Exception as e:
                # Handle other potential file I/O errors (e.g., permission issues)
                print(f"Error loading config file: {e}")
                print("Initializing with default settings.")
                self.config_data = self._get_default_config()
        else:
            # File doesn't exist, so initialize with defaults
            print(f"Config file not found: {self.config_file_path}. Initializing with default settings.")
            self.config_data = self._get_default_config()

    def save_config(self):
        """
        Saves the current in-memory configuration data to the config file.
        """
        try:
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4) # Use indent for human-readability
            print(f"Configuration saved to: {self.config_file_path}")
            return True # Success
        except Exception as e:
            # Handle potential file I/O errors during saving
            print(f"Error saving config file: {e}")
            return False # Failed

    def get_setting(self, key, default_value=None):
        """
        Retrieves a setting by key.
        Returns a default_value if the key is not found.
        """
        parts = key.split('.')
        current = self.config_data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default_value # Key not found at this level
        return current

    def set_setting(self, key, value):
        """
        Sets a setting's value, supporting nested keys using dot notation.
        Creates nested dictionaries if they don't exist.
        """
        parts = key.split('.')
        current = self.config_data
        for i, part in enumerate(parts):
            if i == len(parts) - 1: # Last part of the key
                current[part] = value
            else:
                # If the current part is not a dict or doesn't exist, create an empty dict
                if part not in current or not isinstance(current[part], dict):
                    current[part] = {}
                current = current[part] # Move deeper into the nested structure

    def _get_default_config(self):
        """
        Defines the default structure and values for the application's configuration.
        This is used when no config file exists or when it's corrupted.
        """ 
        return {
            "title": "Title",
            "date": "",
            "description": "Default descriptions for the diary entries.",
            "dynamic_rows": [] # List of dynamic rows for diary entries
        }