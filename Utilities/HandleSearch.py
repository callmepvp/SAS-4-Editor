from Utilities.UtilFunctions import gunIDMap

from colorama import Fore
import msvcrt
import os

def displayWithoutOptions(title): #COPY
        from main import cmd_title, version, dev
        cmd_title(title)

        print(f'''{Fore.RED}
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  ░▒▓█▓▒░   ░▒▓██████▓▒░  ░▒▓██████▓▒░  
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓██▓▒░   ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                 { Fore.LIGHTRED_EX }version: { version } | made by: { dev }{Fore.LIGHTWHITE_EX}''')

def search_guns(query: str) -> dict:
    """Search for guns matching the query."""
    query = query.lower()
    results = {k: v for k, v in gunIDMap.items() if query in v.lower() or query in str(k)}
    return results

def display_results(query: str, results: dict, page: int, page_size: int = 10):
    """Display the search results."""
    os.system('cls')  # Clear the screen
    displayWithoutOptions("Searching weapons...")

    print(f"Search: {query}")
    if not results:
        print(f"{ Fore.LIGHTRED_EX }No matches found.{Fore.LIGHTWHITE_EX}")
    else:
        start_index = page * page_size
        end_index = start_index + page_size
        paginated_results = list(results.items())[start_index:end_index]
        
        print(f"{Fore.LIGHTGREEN_EX}Matches found:{Fore.LIGHTWHITE_EX}")
        for idx, (id, name) in enumerate(paginated_results, start=1 + start_index):
            print(f"{idx}. {id}: {name}")

        print("\nPress 'F1' to confirm selection.")
        
        if end_index < len(results):
            print("Press 'F2' for next page.")
        if start_index > 0:
            print("Press 'F3' for previous page.")

def display_selection_menu(results: dict):
    """Display a menu for the user to select an option from the results."""
    print("\nSelect an option by entering the corresponding number:")
    for idx, (id, name) in enumerate(results.items(), start=1):
        print(f"{idx}. {id}: {name}")
    
    while True:
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(results):
            selected_id = list(results.keys())[int(choice) - 1]
            print(f"You selected: {selected_id} - {results[selected_id]}")
            return selected_id
        else:
            print("Invalid choice, please try again.")

def search_interface():
    """Interactive search interface."""
    query = ""
    page = 0
    page_size = 10

    while True:
        results = search_guns(query)
        start_index = page * page_size
        end_index = start_index + page_size
        paginated_results = list(results.items())[start_index:end_index]
        
        display_results(query, results, page, page_size)
        
        key = msvcrt.getch()
        if key == b'\x00':
            key = msvcrt.getch()
            if key == b';':  # F1 key
                if len(paginated_results) == 1:
                    selected_id = paginated_results[0][0]
                    print(f"\nYou selected: {selected_id} - {results[selected_id]}")
                    return selected_id
                elif len(paginated_results) > 1:
                    return display_selection_menu(dict(paginated_results))
                else:
                    print("\nNo matches to select.")
            elif key == b'<':  # Next page
                if (page + 1) * page_size < len(results):
                    page += 1
            elif key == b'=':  # Previous page
                if page > 0:
                    page -= 1
        elif key == b'\x08':  # Backspace
            query = query[:-1]
            page = 0  # Reset to the first page
        elif key == b'\r':  # Enter
            continue
        else:
            try:
                query += key.decode()
                page = 0  # Reset to the first page
            except UnicodeDecodeError:
                continue  # Ignore the special characters