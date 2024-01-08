import json
import os

def load_json_config(file_path):
    """
    Load a JSON configuration file.
    
    :param file_path: Path to the JSON file.
    :return: Dictionary with the configuration.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON format in file: {file_path}")

def save_json_config(data, file_path):
    """
    Save a dictionary to a JSON configuration file.
    
    :param data: Dictionary with the data to save.
    :param file_path: Path to the JSON file where the data will be saved.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise Exception(f"Error saving JSON config: {str(e)}")

def create_directory_if_not_exists(directory_path):
    """
    Create a directory if it does not exist.
    
    :param directory_path: Path to the directory to be created.
    """
    os.makedirs(directory_path, exist_ok=True)

def update_project_settings(key, value):
    """
    Update a specific setting in the project settings JSON file.
    
    :param key: The key in the settings file to update.
    :param value: The new value to set for the key.
    """
    settings_path = 'config/project_settings.json'
    settings = load_json_config(settings_path)
    settings[key] = value
    save_json_config(settings, settings_path)

# Example usage:
# try:
#     config = load_json_config('config/api_keys.json')
#     print(config['OpenAI_API_Key'])
# except Exception as e:
#     print(e)

# create_directory_if_not_exists('logs')

# update_project_settings('new_setting', 'new_value')
