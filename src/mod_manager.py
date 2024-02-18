import re
import json
from packaging import version
from src.mod_validator import ModValidator

class InvalidModStringError(Exception):
    pass

class ModManager():
    def __init__(self, input_filename, manifest_filename, modpack_name="MattiasModdedMayhem"):
        self.input_filename = input_filename
        self.manifest_filename = manifest_filename
        self.modpack_name = modpack_name
    
    def read_mods_from_file(self):
        mods_list = []
        with open(self.input_filename, 'r') as file:
            for line in file:
                if ModValidator.validate_mod_string(line):
                    mods_list.append(line.strip())
                else:
                    raise InvalidModStringError(f"Invalid mod string {line}")
        return mods_list

    def read_mods_from_json(self):
        mods_list = []
        with open(self.manifest_filename, 'r') as file:
            data = json.load(file)
            if "dependencies" in data:
                mods_list.extend(data["dependencies"])
                del data["dependencies"]  # Remove existing mods under dependencies
        with open(self.manifest_filename, 'w') as file:
            json.dump(data, file, indent=4)
        return mods_list
    
    def separate_semver(self, mod_list):
        name_semver_dict = {}
        
        for mods in mod_list:
            # Use regular expression to match the last set of numbers separated by dots
            match = re.search(r'([\d.]+)$', mods)
            if match:
                semver = match.group(1)
                name = mods[:-len(semver)].rstrip('-')  # Remove semver and any trailing dashes
                
                # Update dictionary if the current semver is newer than what's already stored
                if name not in name_semver_dict or semver > name_semver_dict[name]:
                    name_semver_dict[name] = semver
                    
        return name_semver_dict

    def generate_new_mod_dict(self, installed_mods, new_mods):
        for mod in new_mods:
            if self.modpack_name in mod:
                continue
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
                print(f"Staging mod {mod} with version {new_mods.get(mod)}")
                installed_mods[mod] = new_mods.get(mod)

        return installed_mods

    def write_mods_to_manifest(self, mods_dict):
        with open(self.manifest_filename, 'r') as file:
            data = json.load(file)
            if "dependencies" not in data:
                data["dependencies"] = []
            for name, semver in mods_dict.items():
                if self.modpack_name in name:
                    continue
                data["dependencies"].append(f"{name}-{semver}")

        with open(self.manifest_filename, 'w') as file:
            json.dump(data, file, indent=4)

