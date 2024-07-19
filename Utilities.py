import os
import json
from prettytable import PrettyTable
from colorama import Fore, Style
from typing import Callable, Optional

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
from typing import Callable, Any, List

def request_input(
    prompt: str, 
    validate_funcs: List[Callable[[str], bool]], 
    transform_func: Callable[[str], Any], 
    exit_command: str = "e"
) -> Any:
    """
    Requests input from the user, validates it using a list of validation functions, transforms it using transform_func,
    and allows for an exit command.

    :param prompt: The prompt message to display to the user.
    :param validate_funcs: A list of functions that take the input as a string and return True if it is valid.
    :param transform_func: A function that takes the input as a string and transforms it to the desired type.
    :param exit_command: The command that will exit the input loop (default is "e").
    :return: The transformed input if all validations pass, or None if the exit command is used.
    """
    while True:
        choice = input(prompt).strip()
        if choice.lower() == exit_command:
            print("Exiting the input process.")
            return None
        
        # Check if all validation functions pass
        if all(validate_func(choice) for validate_func in validate_funcs):
            return transform_func(choice)
        else:
            print("Invalid input! Please try again.")


def is_valid_integer(value: str) -> bool:
    if value.isdigit():
        return int(value) >= 0
    else:
        return False

def is_NZinteger(value: str) -> bool:
    return int(value) > 0
    
def is_less_than(max_value: int) -> Callable[[str], bool]:
    """Return a validation function that checks if the value is less than max_value."""
    def validate(value: str) -> bool:
        return int(value) < max_value
    return validate

def is_valid_id(value: str) -> bool:
    """Check if the value is a valid ID in the gunIDMap."""
    if value.isdigit():
        id_value = int(value)
        return id_value in gunIDMap
    return False

def is_valid_name(value: str) -> bool:
    """Check if the value is a valid name in the gunIDMap."""
    return value in gunIDMap.values()

def to_integer(value: str) -> int:
    return int(value)

def is_non_empty_string(value: str) -> bool:
    return bool(value.strip())

def to_string(value: str) -> str:
    return value.strip()

def transform_to_id(value: str) -> Optional[int]:
    """Transform the value to an ID. Returns the ID if the value is valid, or None if invalid."""
    if value.isdigit():
        id_value = int(value)
        if id_value in gunIDMap:
            return id_value
    elif is_valid_name(value):
        # Find the ID corresponding to the name
        for id_value, name in gunIDMap.items():
            if name == value:
                return id_value
    return None

def get_gun_name_from_id(gun_id: int) -> str:
    return gunIDMap.get(gun_id, "Unknown Gun")

def displayWeapons(weapons, columns_per_page=7):
    # Extract all possible keys from the dictionaries to use as table columns
    all_keys = set()
    for weapon in weapons:
        all_keys.update(weapon.keys())
    
    # Ensure 'ID' and 'Name' are the first columns, followed by other columns
    all_keys.discard('ID')
    columns = sorted(all_keys)
    
    # Add ID and Name to the first page columns
    first_page_columns = ['ID', 'Name'] + columns[:columns_per_page - 2]
    
    # Split remaining columns into chunks for subsequent pages
    remaining_columns = columns[columns_per_page - 2:]
    column_chunks = [remaining_columns[i:i + columns_per_page] for i in range(0, len(remaining_columns), columns_per_page)]
    
    # Print the first page
    table = PrettyTable()
    table.field_names = first_page_columns
    
    for weapon in weapons:
        name = gunIDMap.get(weapon.get('ID'), 'Unknown')
        row = [weapon.get('ID', '-'), name] + [weapon.get(col, 'N/A') for col in first_page_columns[2:]]
        table.add_row(row)
    
    print("\n--- Page 1 ---")
    print(table)
    
    # Print the subsequent pages
    for chunk_index, chunk in enumerate(column_chunks):
        table = PrettyTable()
        table.field_names = chunk
        
        for weapon in weapons:
            row = [weapon.get(col, 'N/A') for col in chunk]
            table.add_row(row)

        print("\n\n--- Page {} ---".format(chunk_index + 2))
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