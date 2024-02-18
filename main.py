
import sys
import json
from src import ModValidator, FileSelector
from src.mod_manager import ModManager, InvalidModStringError

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


if __name__ == '__main__':
    input_filename = FileSelector.select_file("Select input file", filetypes=(("Text File", "*.txt"),))
    if input_filename is not None:
        print(f"Selected input file {input_filename}")
    else:
        print("File selection canceled by user")
        sys.exit(1)

    if query_yes_no("Do you want to generate a new manifest file?"):
        manifest_filename = input("Name of manifest file: ")
        while not ModValidator.validate_manifest_filename(manifest_filename):
            print("Invalid file name for manifest file, please enter a valid file name!")
            manifest_filename = input("Name of manifest file: ")

        if not manifest_filename.endswith('.json'):
            manifest_filename += '.json'

        modpack_name = input("Name of mod/modpack: ")
        while not ModValidator.validate_modpack_name(modpack_name):
            print("Invalid name for mod/modpack, please enter a valid name!")
            modpack_name = input("Name of mod/modpack: ")

        version_number = input("Version number (format: x.y.z): ")
        while not ModValidator.validate_version(version_number):
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
        manifest_filename = FileSelector.select_file("Select manifest file", filetypes=(("Json File", "*.json"),))
        if manifest_filename is not None:
            print(f"Selected input file {manifest_filename}")
        else:
            print("File selection canceled by user")
            sys.exit(1)

    mod_manager = ModManager(input_filename, manifest_filename)

    try:
        mods_raw = mod_manager.read_mods_from_file()
    except InvalidModStringError as e:
        print("Error:", e)
        sys.exit(1)

    mods_and_semver_dict = mod_manager.separate_semver(mods_raw)
    old_mods_raw = mod_manager.read_mods_from_json()
    old_mods_and_semver_dict = mod_manager.separate_semver(old_mods_raw)
    new_mod_dict = mod_manager.generate_new_mod_dict(old_mods_and_semver_dict, mods_and_semver_dict)
    mod_manager.write_mods_to_manifest(new_mod_dict)