import copy
import time
from colorama import Fore

from Utilities.UtilFunctions import *
from Utilities.HandleSearch import search_interface
from Utilities.HandleLifecycle import *

class Menu:
    def __init__(self, title, options, optionalText = None):
        self.title = title
        self.options = options
        self.labels = generate_labels(len(options))
        self.optionalText = optionalText
        
    def display(self):
        clear_screen()
        cmd_title(self.title)

        disable_resizing()
        set_console_size(800, 400)
        print(f'''{Fore.RED}
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░  ░▒▓██████▓▒░  
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓██▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                 { Fore.LIGHTRED_EX }version: { version } | made by: { dev }{Fore.LIGHTWHITE_EX}''')
        
        if self.optionalText is not None:
            if self.optionalText[1] is not None:
                print(self.optionalText[1])
            if self.optionalText[0] is not None:
                displayWeapons(self.optionalText[0])

        for label, (description, _) in zip(self.labels, self.options.values()):
            print(f"{Fore.GREEN}{label}. {description}{Fore.LIGHTWHITE_EX}")

    def handle_choice(self):
        while True:
            self.display()
            choice = input("Enter the label of your choice (Type 'e' to go back): ").upper()

            if choice.lower() == "e":
                print("Exiting. Performing cleanup.")
                break

            if choice in self.labels:
                selected_index = self.labels.index(choice)
                selected_key = list(self.options.keys())[selected_index]
                description, selected_function = self.options[selected_key]
                print(f"You selected: {description}")
                time.sleep(1)
                selected_function()
            else:
                print(f"{Fore.LIGHTRED_EX}Invalid input!{Fore.LIGHTWHITE_EX}")
                time.sleep(1)

def displayWithoutOptions(title):
        clear_screen()
        cmd_title(title)

        disable_resizing()
        set_console_size(800, 400)
        print(f'''{Fore.RED}
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░  ░▒▓██████▓▒░  
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓██▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                 { Fore.LIGHTRED_EX }version: { version } | made by: { dev }{Fore.LIGHTWHITE_EX}''')

def generate_labels(num_options):
    labels = []
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in range(num_options):
        letter = alphabet[i // 9]
        number = (i % 9) + 1
        labels.append(f"{letter}{number}")
    return labels

def option(description):
    def decorator(func):
        return description, func
    return decorator

#* MENUS
@option("Change Money.")
def changeMoney():
    while True:
        displayWithoutOptions("Change Money")

        json_data = readJSONFile("decoded_profile.json")
        moneyData = json_data['Inventory']['Profile0']['Money']
        print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} You currently have {moneyData} cash!")
        choice = input("Enter new money amount (or 'e' to go back): ")
        if choice.lower() == "e":
            break
        if checkInteger(choice):
            updateJSONField('decoded_profile.json', 'Inventory.Profile0.Money', int(choice))
            time.sleep(2)
        else:
            print(f"{Fore.LIGHTRED_EX}Invalid input!{Fore.LIGHTWHITE_EX}")
            time.sleep(1)

@option("Change Loadout.")
def changeLoadout():
    loadout_menu = Menu("Change Loadout", {
        "editWeapon": editWeapon,
        "editEquipment": editEquipment
    })
    loadout_menu.handle_choice()

@option("Edit Weapon.")
def editWeapon():
    json_data = readJSONFile("decoded_profile.json")
    weaponData = json_data['Inventory']['Profile0']['Weapons']

    #Get all weapons
    weapons = []
    for item in weaponData:
        weapons.append(item)

    loadout_menu = Menu("Edit Weaponry", {
        "Edit existing weapon": editExistingWeapon,
        "Add new weapon": addNewWeapon
    }, [weapons, f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Your current setup: "])
    loadout_menu.handle_choice()

@option("Edit Existing Weapon.")
def editExistingWeapon():
    displayWithoutOptions("Edit Existing Weapon")
    choice = input(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Input the 'Identifier' number of the weapon: ")

@option("Add New Weapon.")
def addNewWeapon():
    displayWithoutOptions("Edit Existing Weapon")
    json_data = readJSONFile("decoded_profile.json")
    weaponData = json_data['Inventory']['Profile0']['Weapons']
    gunData = copy.deepcopy(gunDataSet) #Deep copy the gun data set

    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Gun template created.")

    #Request the info
    """gunData['ID'] = request_input(
        f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Input the NAME or ID of the weapon: ",
        [lambda x: is_valid_id(x, "#GUN") or is_valid_name(x, "#GUN")], 
        lambda x: transform_to_id(x, "#GUN")   
    )"""
    selectedID = search_interface()
    gunData['ID'] = int(selectedID)
    
    if gunData['ID'] is None: 
        return

    gunData['Grade'] = request_input(
        f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Input the GRADE of the weapon [0-12]: ",
        [is_valid_integer, is_less_than(13)],
        to_integer 
    )
    
    if gunData['Grade'] is None:
        return
    
    gunData['AugmentSlots'] = request_input(
        f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Input the amount of AUGMENT SLOTS [0-4]: ",
        [is_valid_integer, is_less_than(5)],
        to_integer 
    )
    
    if gunData['AugmentSlots'] is None:
        return
    
    #Deal with augment data
    if gunData['AugmentSlots'] != 0:
        print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} For every augment slot ({gunData['AugmentSlots']}), choose its level and type (ID!): ")
        for i in range(1, gunData['AugmentSlots'] + 1):
            gunData[f"Augment{i}ID"] = request_input(
                f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Type for slot {i} [1-11]: ",
                [lambda x: is_valid_id(x, "#AUG") or is_valid_name(x, "#AUG")],
                lambda x: transform_to_id(x, "#AUG")
            )

            gunData[f"Augment{i}LVL"] = request_input(
                f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Level for slot {i} [0-Grade]: ",
                [is_valid_integer, is_less_than(gunData["Grade"]+1)],
                to_integer
            )

    #Add gun data to main data
    highestInvIndex = len(weaponData) - 1 #Minus 1 for index
    gunData['InventoryIndex'] = highestInvIndex + 1
    gunData['Seen'] = True

    weaponData.append(gunData)
    updateJSONField("decoded_profile.json", "Inventory.Profile0.Weapons", weaponData)

    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Successfully created weapon '{gunIDMap.get(gunData['ID'])}'.")
    time.sleep(3)

@option("Edit Equipment.")
def editEquipment():
    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} WIP...")

@option("Save And Export.")
def saveAndExport():
    pass

@option("View Changelog.")
def viewChangelog():
    displayWithoutOptions("View Changelog")

    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} Changelog:\n")
    
    for entry in changelog_entries:
        print_changelog_entry(entry)

    while True:
        choice = input("Type 'e' to go back: ")
        if choice == 'e':
            break

@option("View Settings.")
def viewSettings():
    pass

#* MAIN
if __name__ == "__main__":
    from Utilities.HandleLifecycle import initiateStartUp
    initiateStartUp()

    #Main Menu
    main_menu = Menu("Main Menu", {
        "changeLoadout": changeLoadout,
        "changeMoney": changeMoney,
        "saveAndExport": saveAndExport,
        "viewChangelog": viewChangelog,
        "viewSettings": viewSettings
    })

    # Run the main menu
    main_menu.handle_choice()
