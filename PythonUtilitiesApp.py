import requests
import os
import winshell
from win32com.client import Dispatch
from tqdm import tqdm

GITHUB_API_URL = "https://api.github.com/repos/Stari-Div/Python-Utilities/releases/latest"

def get_latest_release_tag_name():
    """Get the latest release tag name."""
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()  # Raise an error for bad status codes
    release_data = response.json()
    tag_name = release_data.get("tag_name")
    if not tag_name:
        raise ValueError("No tag name found for the latest release")
    return tag_name

def find_folder_with_tag_name(tag_name, search_path):
    """Search for a folder with 'Python-Utilities-' followed by the tag name in its name within the given directory."""
    search_for = f"Python-Utilities-{tag_name}"
    for root, dirs, files in tqdm(os.walk(search_path), desc="Searching for folder", unit="dir"):
        for dir_name in dirs:
            if search_for in dir_name:
                return os.path.join(root, dir_name)
    return None

def find_file(filename, search_path):
    """Search for a file in the given directory and subdirectories."""
    for root, dirs, files in tqdm(os.walk(search_path), desc=f"Searching for {filename}", unit="file"):
        if filename in files: 
            return os.path.join(root, filename)
    return None

def create_shortcut(target_path, icon_path):
    """Delete any existing shortcut and create a new one on the desktop."""
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "Python Utilities.lnk")

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        print(f"Deleted existing shortcut at {shortcut_path}")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.IconLocation = icon_path
    shortcut.save()
    print(f"Shortcut created at {shortcut_path}")

if __name__ == "__main__":
    # Define the filenames to search for
    filename_to_find = "CentralUI.py"
    icon_filename = "PyUtilitiesIcon.ico"
    root_search_path = "C:/"

    # Get the latest release tag name
    try:
        tag_name = get_latest_release_tag_name()
        print(f"Latest release tag: {tag_name}")
    except ValueError as ve:
        print(f"Failed to get the latest release tag name: {ve}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

    # Search for the folder with the tag name
    release_folder_path = find_folder_with_tag_name(tag_name, root_search_path)
    if release_folder_path:
        print(f"Found folder with tag name: {release_folder_path}")

        # Search for the target file in the release folder
        target_path = find_file(filename_to_find, release_folder_path)
        if target_path:
            print(f"Found {filename_to_find} at {target_path}")

            # Search for the icon file
            icon_path = find_file(icon_filename, release_folder_path)
            if icon_path:
                print(f"Found {icon_filename} at {icon_path}")
            else:
                print(f"{icon_filename} not found. Using default icon.")
                icon_path = target_path  # Use the target file as the icon if the icon file is not found

            # Create or update the shortcut
            create_shortcut(target_path, icon_path)
        else:
            print(f"{filename_to_find} not found in {release_folder_path}")
    else:
        print(f"Folder with tag name {tag_name} not found in {root_search_path}")
