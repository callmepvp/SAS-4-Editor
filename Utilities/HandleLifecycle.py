from ctypes import windll, wintypes
import ctypes
from os import getcwd, system as _sys, name as _name
import time
import winreg
from colorama import Fore
import requests
import json
import os

DEFAULT_CONFIG = { #! LOCAL VERSION HERE
    "REPO_OWNER": "callmepvp",
    "REPO_NAME": "SAS-4-Editor",
    "current_profile": "Profile0",
    "steam_user_id": 76561198299512367,
    "updater": True,
    "version": "1.2"
}

base_path: str = getcwd()
version: str = DEFAULT_CONFIG['version']
dev: str = 'callmepvp @ github'

def initiateStartUp():
    clear_screen()
    cmd_title("Welcome!")

    print(f'''{Fore.RED}
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓██████████████▓▒░░▒▓████████▓▒░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░              
 ░▒▓█████████████▓▒░░▒▓████████▓▒░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░                                                                                                 
          {Fore.LIGHTWHITE_EX}''')

    """Display startup sequence text and perform initial tasks."""
    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} {Fore.LIGHTGREEN_EX}Initializing startup...{Fore.LIGHTWHITE_EX}")
    time.sleep(2)

    #Check file integrity
    ensureConfigExists()
    time.sleep(2)

    #Check save file integrity
    steam_path = findSteamLocation()
    if steam_path:
        #print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} Steam installation found @ {steam_path}")
        user_data_folder = find_user_data_folder(steam_path, "678800")
        if user_data_folder:
            profile_save_path = find_profile_save_folder(user_data_folder)
            if profile_save_path:
                profile_save_path += "\Profile.save"
                print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} Path to 'Profile.save': {profile_save_path}")
                print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} Save file path verified." if os.path.isfile(profile_save_path) else f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} Save path file not verified.")
            else:
                print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} File 'Profile.save' not found.")
        else:
            print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} Game folder '678800' not found.")
    else:
        print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} Steam installation not found.")
    
    time.sleep(2)

    #! ALSO CHECK FOR RUNNING SAVES AND LOGS/SESSIONS IF THE PROGRAM DIDNT EXIT PROPERLY

    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} {Fore.LIGHTGREEN_EX}Checking for updates...{Fore.LIGHTWHITE_EX}")
    time.sleep(1)

    #Check updates
    checkForUpdates()
    time.sleep(2)

    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} {Fore.LIGHTGREEN_EX}Cleaning up and starting...{Fore.LIGHTWHITE_EX}")
    time.sleep(2)

    print(f"{Fore.RED}[VORTEX]{Fore.LIGHTWHITE_EX} {Fore.LIGHTGREEN_EX}All good!{Fore.LIGHTWHITE_EX}")
    time.sleep(2)

#* CMD UTILS
def cmd_title(title: str) -> None:
    return windll.kernel32.SetConsoleTitleW(f'Vortex ver. {version} | {title}')

def clear_screen():
    _sys('cls' if _name == 'nt' else 'clear')

def set_console_size(width, height):
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd == 0:
        raise Exception("Failed to get console window handle")

    hStdOut = ctypes.windll.kernel32.GetStdHandle(-11)
    buffer_size = wintypes._COORD(width, height)
    ctypes.windll.kernel32.SetConsoleScreenBufferSize(hStdOut, buffer_size)

    rect = ctypes.wintypes.SMALL_RECT(0, 0, width - 1, height - 1)
    ctypes.windll.kernel32.SetConsoleWindowInfo(hStdOut, True, ctypes.byref(rect))

def disable_resizing():
    hWnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hWnd == 0:
        raise Exception("Failed to get console window handle")

    GWL_STYLE = -16
    WS_SIZEBOX = 0x00040000
    style = ctypes.windll.user32.GetWindowLongW(hWnd, GWL_STYLE)
    style &= ~WS_SIZEBOX
    ctypes.windll.user32.SetWindowLongW(hWnd, GWL_STYLE, style)
    ctypes.windll.user32.SetWindowPos(hWnd, None, 0, 0, 0, 0, 0x0027)  # SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED

#* UPDATE UTILS
def load_config():
    """Load configuration from the JSON file."""
    with open("config.json", 'r') as file:
        config = json.load(file)
        return config['REPO_OWNER'], config['REPO_NAME']
    
def get_remote_version(repo_owner, repo_name):
    """Fetch the latest version tag from the GitHub repository."""
    url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/master/config.json"
 
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['version']  # Latest release tag
    else:
        raise Exception("Failed to fetch remote version")

def checkForUpdates():
    """Check if the local version is up to date."""
    local_version = version
    try:
        repo_owner, repo_name = load_config()
        remote_version = get_remote_version(repo_owner, repo_name)
        if local_version == remote_version:
            print(f"{Fore.LIGHTBLUE_EX}[UPDATER]{Fore.LIGHTWHITE_EX} Your application is up-to-date.")
        else:
            print(f"{Fore.LIGHTBLUE_EX}[UPDATER]{Fore.LIGHTWHITE_EX} Update available! Local version: {local_version}, Remote version: {remote_version}")
    except Exception as e:
        print(f"{Fore.LIGHTBLUE_EX}[UPDATER]{Fore.LIGHTWHITE_EX} Error checking for updates: {e}")

#* OTHER UTILS
def ensureConfigExists():
    """Check if config.json exists and create it with default content if not."""
    if not os.path.isfile("config.json"):
        print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} 'config.json' not found. Creating with default settings.")
        with open("config.json", 'w') as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} 'config.json' created with default settings.")
    else:
        print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} 'config.json' already exists.")

def is_steam_directory(path):
    """Check if the given directory is a valid Steam installation."""
    # Check if the path is a directory
    if not os.path.isdir(path):
        return False
    
    # Check for steam.exe and steamapps folder
    files_and_dirs = os.listdir(path)
    if "steam.exe" in files_and_dirs and "steamapps" in files_and_dirs:
        return True

    return False

def find_profile_save_folder(user_data_folder: str) -> str:
    """Search through local -> Data -> Docs to find the directory containing Profile.save."""
    target_path = os.path.join(user_data_folder, '678800', 'local', 'Data', 'Docs')
    
    if not os.path.isdir(target_path):
        print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} Target path does not exist.")
        return None
    
    # Iterate through all subdirectories in Docs
    for root, dirs, files in os.walk(target_path):
        if 'Profile.save' in files:
            return root
    
    return None

def find_user_data_folder(steam_path: str, target_folder: str) -> str:
    """Search through the Steam userdata folder to find the specific target folder."""
    user_data_path = os.path.join(steam_path, 'userdata')
    
    if not os.path.isdir(user_data_path):
        print(f"{Fore.LIGHTBLUE_EX}[INTEGRITY]{Fore.LIGHTWHITE_EX} Userdata folder does not exist.")
        return None
    
    # Iterate through all subdirectories in userdata
    for user_folder in os.listdir(user_data_path):
        user_folder_path = os.path.join(user_data_path, user_folder)
        
        if not os.path.isdir(user_folder_path):
            continue
        
        # Check if the target folder exists within this user folder
        target_folder_path = os.path.join(user_folder_path, target_folder)
        if os.path.isdir(target_folder_path):
            return user_folder_path
    
    return None

def findSteamLocation():
    # Check common paths
    common_paths = [
        "C:\\Program Files (x86)\\Steam",
        "C:\\Program Files\\Steam",
        "D:\\Program Files (x86)\\Steam",
        "D:\\Program Files\\Steam",
        "E:\\Program Files (x86)\\Steam",
        "E:\\Program Files\\Steam",
        "F:\\Program Files (x86)\\Steam",
        "F:\\Program Files\\Steam",
        "C:\\Steam",
        "D:\\Steam",
        "E:\\Steam",
        "F:\\Steam"
    ]
    
    # First, check common paths
    for path in common_paths:
        if is_steam_directory(path):
            return path
    
    # If not found, check registry
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as key:
            steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
            if is_steam_directory(steam_path):
                return steam_path
    except (FileNotFoundError, ImportError):
        pass
    
    return None