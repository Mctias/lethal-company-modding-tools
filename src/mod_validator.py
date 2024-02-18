import re
import os

class ModValidator:
    @staticmethod
    def validate_mod_string(mod_string):
        pattern = r'^[a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+-\d+\.\d+\.\d+$'
        return re.match(pattern, mod_string) is not None

    @staticmethod
    def validate_version(version):
        pattern = r'\d+\.\d+\.\d+'  # Validates x.y.z format
        return bool(re.match(pattern, version))

    @staticmethod
    def validate_modpack_name(input_string):
        if not input_string:  # Check if the string is empty
            return False
        if ' ' in input_string:  # Check if the string contains any spaces
            return False
        return True

    @staticmethod
    def validate_manifest_filename(filename):
        if not filename:  # Check if the filename is empty
            return False
        if any(char in r'\/:*?"<>|' for char in filename):  # Check for invalid characters
            return False
        if len(filename) > 255:  # Check if the filename exceeds the maximum length
            return False
        if os.path.exists(filename):  # Check if the filename already exists
            return False
        return True