import os
import json
from prettytable import PrettyTable
from colorama import Fore, Style
from typing import Callable

#* DATA SETS
gunDataSet = {
"ID": 0,
"EquipVersion": 0,
"Grade": 0,
"EquippedSlot": -1,
"AugmentSlots": 0,
"InventoryIndex": 0,
"Seen": False,
"BonusStatsLevel": 0,
"ContainsKey": False,
"ContainsAugmentCore": False,
"BlackStrongboxSeed": 0,
"UseDefaultOpenLogic": True
}

gunIDMap = {
    6: "Trailblazer",
    7: "CM 401 Planet Stormer",
    8: "RIA T7",
    9: "RIA 313",
    10: "Ronson 65-a",
}

#* UTIL FUNCTIONS
def request_input(prompt: str, validate_func: Callable[[str], bool], transform_func: Callable[[str], any]) -> any:
    while True:
        choice = input(prompt)
        if choice.lower() == "e":
            print("Exiting the input process.")
            return None
        if validate_func(choice):
            return transform_func(choice)
        else:
            print("Invalid input! Please try again.")

def is_integer(value: str) -> bool:
    return value.isdigit()

def to_integer(value: str) -> int:
    return int(value)

def is_non_empty_string(value: str) -> bool:
    return bool(value.strip())

def to_string(value: str) -> str:
    return value.strip()

def get_gun_name_from_id(gun_id: int) -> str:
    return gunIDMap.get(gun_id, "Unknown Gun")

def displayWeapons(weapons):
    # Create a PrettyTable object
    table = PrettyTable()
    
    # Extract all possible keys from the dictionaries to use as table columns
    columns = set()
    for weapon in weapons:
        columns.update(weapon.keys())
    
    # Ensure 'ID' is the first column, followed by other columns
    if 'ID' in columns:
        columns.remove('ID')
        columns = ['ID', 'Name'] + sorted(columns)
    else:
        columns = ['Name'] + sorted(columns)
    
    # Set the table columns
    table.field_names = columns
    
    # Add rows to the table
    for weapon in weapons:
        # Fetch the weapon name using the ID-to-name dictionary
        name = gunIDMap.get(weapon.get('ID'), 'Unknown')
        row = [weapon.get('ID', '-'), name] + [weapon.get(col, '-') for col in table.field_names[2:]]
        table.add_row(row)
    
    # Print the table
    print(table)

def checkInteger(input):
    try:
        input = int(input)
        if input >= 0:
            return True
        else:
            return False
    except:
        return False

def readJSONFile(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def updateJSONField(file_path: str, field_path: str, new_value):
    """
    Update a specific field in a JSON file with new data.

    :param file_path: Path to the JSON file.
    :param field_path: Dot-separated string representing the field path to update (e.g., "Inventory.Profile0.Weapons").
    :param new_value: The new value to set at the specified field path.
    :return: None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Split the field path into keys
    keys = field_path.split('.')
    
    # Navigate to the field
    target = data
    for key in keys[:-1]:
        if key not in target:
            raise KeyError(f"Key '{key}' not found in the JSON structure.")
        target = target[key]
    
    # Update the field with the new value
    last_key = keys[-1]
    if last_key not in target:
        raise KeyError(f"Key '{last_key}' not found in the JSON structure.")
    target[last_key] = new_value

    # Save the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Successfully updated '{field_path}' to '{new_value}'.")