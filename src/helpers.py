import json
import os

class Helpers:
    def get_value_from_json(file_path, key_to_retrieve) -> str:
        """Retrieve the value of the specified key from the JSON file."""
        if not os.path.exists(file_path):
            print(f"File '{file_path}' not found.")
            return None
        
        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except IOError as e:
            print(f"Error reading file: {e}")
            return None

        if key_to_retrieve in json_data:
            return json_data[key_to_retrieve]
        else:
            print(f"'{key_to_retrieve}' key not found in the JSON data.")
            return None

    # This method does not work with nested keys since I can't be bothered :)
    def update_json_value(file_path, key_to_update, new_value) -> bool:
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        if key_to_update in json_data:
            json_data[key_to_update] = new_value
            print(f"'{key_to_update}' updated to: {new_value}")
        else:
            print(f"'{key_to_update}' key not found in the JSON data.")
            return False
        
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)
            print("JSON file updated successfully.")
            return True

    def increment_major_version(version_str, increments=1):
        """Increment the patch version of a semantic version string."""
        try:
            # Split the version string into major, minor, and patch
            major, minor, patch = map(int, version_str.split('.'))
        except ValueError:
            raise ValueError("Version number is not in the correct format. Expected format: X.Y.Z")

        # Increment the patch version
        major += increments
        minor = 0
        patch = 0
        
        # Return the updated version string
        return f"{major}.{minor}.{patch}"
    
    def increment_minor_version(version_str, increments=1):
        """Increment the patch version of a semantic version string."""
        try:
            # Split the version string into major, minor, and patch
            major, minor, patch = map(int, version_str.split('.'))
        except ValueError:
            raise ValueError("Version number is not in the correct format. Expected format: X.Y.Z")

        # Increment the patch version
        minor += increments
        patch = 0
        
        # Return the updated version string
        return f"{major}.{minor}.{patch}"
    
    def increment_patch_version(version_str, increments=1):
        """Increment the patch version of a semantic version string."""
        try:
            # Split the version string into major, minor, and patch
            major, minor, patch = map(int, version_str.split('.'))
        except ValueError:
            raise ValueError("Version number is not in the correct format. Expected format: X.Y.Z")

        # Increment the patch version
        patch += increments
        
        # Return the updated version string
        return f"{major}.{minor}.{patch}"





