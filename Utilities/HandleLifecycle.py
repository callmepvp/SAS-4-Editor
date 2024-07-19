from ctypes import windll, wintypes
import ctypes
from os import getcwd, system as _sys, name as _name
import time
from colorama import Fore
import requests
import json

base_path: str = getcwd()
version: str = '1.2'
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
    print(f"{Fore.LIGHTGREEN_EX}Initializing startup...{Fore.LIGHTWHITE_EX}")
    time.sleep(2)

    print(f"{Fore.LIGHTGREEN_EX}Checking for updates...{Fore.LIGHTWHITE_EX}")
    time.sleep(1)

    print(f"{Fore.LIGHTGREEN_EX}Starting application...{Fore.LIGHTWHITE_EX}")
    time.sleep(1)

    print(f"{Fore.LIGHTGREEN_EX}All good!{Fore.LIGHTWHITE_EX}")
    time.sleep(1)

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
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['tag_name']  # Latest release tag
    else:
        raise Exception("Failed to fetch remote version")

def check_for_updates():
    """Check if the local version is up to date."""
    local_version = version
    try:
        repo_owner, repo_name = load_config()
        remote_version = get_remote_version(repo_owner, repo_name)
        if local_version == remote_version:
            print("Your application is up-to-date.")
        else:
            print(f"Update available! Local version: {local_version}, Remote version: {remote_version}")
    except Exception as e:
        print(f"Error checking for updates: {e}")