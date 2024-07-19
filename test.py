import json

import requests
version = "1.2"


def load_config():
    """Load configuration from the JSON file."""
    with open("config.json", 'r') as file:
        config = json.load(file)
        return config['REPO_OWNER'], config['REPO_NAME']
    
def get_remote_version(repo_owner, repo_name):
    """Fetch the latest version tag from the GitHub repository."""
    #url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    url = f"https://raw.githubusercontent.com/callmepvp/SAS-4-Editor/master/config.json"
    print(url)
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['version']  # Latest release tag
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

check_for_updates()