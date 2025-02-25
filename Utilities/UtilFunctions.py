import os
import json
from prettytable import PrettyTable
from colorama import Fore, Style
from typing import Callable, Optional, List, Dict

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
    11: "CM 307",
    12: "Sub-light COM2",
    13: "Stripper",
    14: "RIA 20 Para",
    15: "CM Gigavolt",
    16: "Poison Claw",
    17: "HVM 002",
    18: "Ronson WP Flamethrower",
    19: "Ronson 55",
    20: "CM 505",
    21: "CM 205",
    22: "HVM 001",
    23: "CM 202",
    24: "CM 351 Sunflare",
    25: "Ronson LBM",
    26: "Mixmaster",
    28: "Hard Thorn",
    29: "RIA 30 Strikeforce",
    30: "RIA 7",
    31: "HVM 005 G-Class",
    33: "Gebirgskanone",
    34: "HVM MPG",  
    35: "HVM 004",
    36: "CM 451 Starburst",
    37: "Ronson 45",
    38: "HVM 008",
    39: "HIKS S300",
    40: "T-101 Feldhaubitz",
    41: "RIA 20 Striker",
    43: "RIA 50",
    44: "T-102 Jagdfaust",
    61: "1887 Shockfield",
    66: "1887 Shockfield [RED]",
    67: "Sabre [RED]",
    68: "Mustang [RED]",
    69: "RIA 20 DSC [RED]",
    70: "CM 205 [RED]",
    71: "CM 451 Starburst [RED]",
    72: "RIA 20 DSC",
    73: "HVM MPG [RED]",
    74: "Ronson WP Flamethrower [RED]",
    75: "CM 202 [RED]",
    76: "Mixmaster [RED]",
    77: "Ronson 45 [RED]",
    78: "HVM 001 [RED]",
    79: "RIA 20 Para [RED]",
    80: "CM 505 [RED]",
    81: "Hornet [RED]",
    82: "HIKS S300 [RED]",
    83: "Hornet",
    84: "Sabre",
    85: "Stripper [RED]",
    86: "HVM 005 G-Class [RED]",
    87: "CM 351 Sunflare [RED]",
    88: "Raptor [RED]",
    89: "Phantom",
    90: "Raptor",
    91: "Gebirgskanone [RED]",
    92: "T-102 Jagdfaust [RED]",
    93: "Sub-light COM2 [RED]",
    94: "HVM 002 [RED]",
    95: "HVM 008 [RED]",
    96: "RIA 30 Strikeforce [RED]",
    97: "RIA 7 [RED]",
    98: "Mustang",
    99: "Hard Thorn [RED]",
    100: "Ronson 65-a [RED]",
    101: "HVM 004 [RED]",
    102: "RIA 20 Striker [RED]",
    103: "RIA T7 [RED]",
    104: "Ronson LBM [RED]",
    105: "Ronson 55 [RED]",
    106: "Phantom [RED]",
    107: "RIA 50 [RED]",
    108: "T-101 Feldhaubitz [RED]",
    109: "CM 401 Planet Stormer [RED]",
    110: "RIA 313 [RED]",
    111: "Poison Claw [RED]",
    112: "Supermarine [RED]",
    113: "CM 307 [RED]",
    114: "Supermarine",
    115: "CM Gigavolt [RED]",
    116: "Trailblazer [RED]"
}

augmentIDMap = {
    1: "Deadly",
    2: "Piercing",
    3: "Adaptive",
    4: "Enlarged",
    5: "Pinpoint",
    6: "Overclocked",
    7: "Tenacious",
    8: "Capacity",
    9: "Race Modded",
    10: "Skeletonized",
    11: "Biosynthesis"
}

changelog_entries: List[Dict[str, str]] = [
    {
        "version": "1.2",
        "date": "20.07.24",
        "changes": [
            "Finished the feature of adding new weapons.",
            "Prettified the GUI.",
            "Added search feature for weapons.",
            "Added the changelog."
        ]
    },
    {
        "version": "1.1",
        "date": "19.07.24",
        "changes": [
            "Added the basics of adding new weaponry."
        ]
    },
    {
        "version": "1.0",
        "date": "19.07.24",
        "changes": [
            "Added main code and basic encoding/decoding."
        ]
    }
]

#* UTIL FUNCTIONS
def print_changelog_entry(entry: Dict[str, str]):
    """Print a single changelog entry."""
    print(f"{Fore.LIGHTCYAN_EX}Version {entry['version']}{Fore.LIGHTWHITE_EX} | {Fore.LIGHTMAGENTA_EX}{entry['date']}{Fore.LIGHTWHITE_EX}")
    for change in entry['changes']:
        print(f"» {change}")
    print()

def request_input(prompt: str, validate_funcs: List[Callable[[str], bool]], transform_func: Callable[[str], any]) -> any:
    """Request input from the user with validation and transformation."""
    while True:
        choice = input(prompt)
        if choice.lower() == "e":
            print("Exiting the input process.")
            return None
        
        # Check all validation functions
        if all(func(choice) for func in validate_funcs):
            transformed_value = transform_func(choice)
            if transformed_value is not None:
                return transformed_value
            else:
                print("Transformation failed. Please try again.")
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

def is_valid_id(value: str, type: str) -> bool:
    """Check if the value is a valid ID in the given map."""
    if value.isdigit():
        id_value = int(value)

        if type == "#GUN":
            return id_value in gunIDMap
        elif type == "#AUG":
            if is_NZinteger(value) and is_less_than(12):
                return id_value in augmentIDMap
            else:
                return False
        else:
            return False
    return False

def is_valid_name(value: str, type: str) -> bool:
    """Check if the value is a valid name in the given map."""
    if type == "#GUN":
        return value in gunIDMap.values()
    elif type == "#AUG":
        return value in augmentIDMap.values()
    else:
        return False

def to_integer(value: str) -> int:
    return int(value)

def is_non_empty_string(value: str) -> bool:
    return bool(value.strip())

def to_string(value: str) -> str:
    return value.strip()

def transform_to_id(value: str, type: str) -> Optional[int]:
    """Transform the value to an ID. Returns the ID if the value is valid, or None if invalid."""
    if type == "#GUN":
        id_map = gunIDMap
    elif type == "#AUG":
        id_map = augmentIDMap
    else:
        return None

    if value.isdigit():
        id_value = int(value)
        if id_value in id_map:
            return id_value
    elif value in id_map.values():
        # Find the ID corresponding to the name
        for id_value, name in id_map.items():
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
    
    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} JSONUpdate function-call successful.")