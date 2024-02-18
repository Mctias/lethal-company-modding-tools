import re
import json
from packaging import version
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

class InvalidModStringError(Exception):
    pass

def read_mods_from_file(file_path):
    mods_list = []
    with open(file_path, 'r') as file:
        for line in file:
            if validate_mod_string(line):
                mods_list.append(line.strip())
            else:
                raise InvalidModStringError(f"Invalid mod string {line}")
    return mods_list

def validate_mod_string(mod_string):
    pattern = r'^[a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+-\d+\.\d+\.\d+$'
    return re.match(pattern, mod_string) is not None

def read_mods_from_json(json_file):
    mods_list = []
    with open(json_file, 'r') as file:
        data = json.load(file)
        if "dependencies" in data:
            mods_list.extend(data["dependencies"])
            del data["dependencies"]  # Remove existing mods under dependencies
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
    return mods_list

def separate_semver(list):
    name_semver_dict = {}
    
    for mods in list:
        # Use regular expression to match the last set of numbers separated by dots
        match = re.search(r'([\d.]+)$', mods)
        if match:
            semver = match.group(1)
            name = mods[:-len(semver)].rstrip('-')  # Remove semver and any trailing dashes
            
            # Update dictionary if the current semver is newer than what's already stored
            if name not in name_semver_dict or semver > name_semver_dict[name]:
                name_semver_dict[name] = semver
                
    return name_semver_dict

def generate_new_mod_dict(installed_mods, new_mods):
    for mod in new_mods:
        if mod in installed_mods:
            # Compare semvers and see if which is newer
            if version.parse(new_mods.get(mod)) > version.parse(installed_mods.get(mod)):
                print(f"Updating {mod} {installed_mods.get(mod)} -> {new_mods.get(mod)}.")
                installed_mods.update({mod: new_mods.get(mod)})
            elif version.parse(new_mods.get(mod)) < version.parse(installed_mods.get(mod)):
                print(f"{mod} already has a newer version installed {installed_mods.get(mod)}. Trying to install {new_mods.get(mod)}. Keeping newest.")
            else:
                print(f"{mod} with version {installed_mods.get(mod)} already exists in provided manifest.")
        else:
            print(f"Adding mod {mod} with version {new_mods.get(mod)}")
            installed_mods[mod] = new_mods.get(mod)

    return installed_mods


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question, prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def write_mods_to_manifest(manifest_file, mods_dict):
    with open(manifest_file, 'r') as file:
        data = json.load(file)
        modpack_name = data["name"]
        if "dependencies" not in data:
            data["dependencies"] = []
        for name, semver in mods_dict.items():
            if modpack_name in name:
                continue
            data["dependencies"].append(f"{name}-{semver}")

    with open(manifest_file, 'w') as file:
        json.dump(data, file, indent=4)

def validate_version(version):
    pattern = r'\d+\.\d+\.\d+'  # Validates x.y.z format
    return bool(re.match(pattern, version))

def validate_modpack_name(input_string):
    if not input_string:  # Check if the string is empty
        return False
    if ' ' in input_string:  # Check if the string contains any spaces
        return False
    return True

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

def select_file(title, filetypes):
    root = Tk()
    root.withdraw()  # Hide the main window

    filename = askopenfilename(title=title, filetypes=filetypes)
    if not filename:  # If the user cancels the dialog, filename will be an empty string
        print("File selection cancelled by user.")
        return None

    return filename


if __name__ == '__main__':
    Tk().withdraw()
    
    input_filename = select_file("Select input file", filetypes=(("Text File", "*.txt"),))
    if input_filename is not None:
        print("Selected input file:", input_filename)
    else:
        print("No file selected, exiting.")
        sys.exit(1)

    try:
        mods_raw = read_mods_from_file(input_filename)
    except InvalidModStringError as e:
        print("Error:", e)
        sys.exit(1)

    if query_yes_no("Do you want to generate a new manifest file?"):
        
        manifest_filename = input("Name of manifest file: ")
        while not validate_manifest_filename(manifest_filename):
            print("Invalid file name for manifest file, please enter a valid file name!")
            manifest_filename = input("Name of manifest file: ")

        if not manifest_filename.endswith('.json'):
            manifest_filename += '.json'

        modpack_name = input("Name of mod/modpack: ")
        while not validate_modpack_name(modpack_name):
            print("Invalid name for mod/modpack, please enter a valid name!")
            modpack_name = input("Name of mod/modpack: ")

        version_number = input("Version number (format: x.y.z): ")
        while not validate_version(version_number):
            print("Invalid version number format! Please use x.y.z format.")
            version_number = input("Version number (format: x.y.z): ")

        # These two can be empty :)
        website_url = input("Website url: ")
        description = input("Description: ")

        manifest_data = {
            "name": modpack_name,
            "version_number": version_number,
            "website_url": website_url,
            "description": description,
            "dependencies": []
        }
        
        print("Creating manifest file...")
        with open(f"{manifest_filename}", 'w') as file:
            json.dump(manifest_data, file, indent=4)
    else: 
        Tk().withdraw() 
        manifest_filename = select_file("Select manifest file", filetypes=(("Json File", "*.json"),))
        if manifest_filename is not None:
            print("Selected mainfest file:", manifest_filename)
        else:
            print("No manifest selected, exiting.")
            sys.exit(1)

    mods_and_semver_dict = separate_semver(mods_raw)
    old_mods_raw = read_mods_from_json(manifest_filename)
    old_mods_and_semver_dict= separate_semver(old_mods_raw)
    new_mod_dict = generate_new_mod_dict(old_mods_and_semver_dict, mods_and_semver_dict)
    write_mods_to_manifest(manifest_filename, new_mod_dict)