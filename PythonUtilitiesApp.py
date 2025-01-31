# pip install winshell pywin32
import os
import winshell
from win32com.client import Dispatch

def find_file(filename, search_path):
    """Search for a file in the given directory and subdirectories."""
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def create_shortcut(target_path, icon_path):
    """Create a shortcut on the desktop."""
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "Python Utilities.lnk")

    if not os.path.exists(shortcut_path):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.IconLocation = icon_path
        shortcut.save()
        print(f"Shortcut created at {shortcut_path}")
    else:
        print("Shortcut already exists")

if __name__ == "__main__":
    # Define the filenames to search for and the root search path
    filename_to_find = "CentralUI.py"
    icon_filename = "Python-Icon.ico"
    root_search_path = "C:/"

    # Search for the target file
    target_path = find_file(filename_to_find, root_search_path)
    if target_path:
        print(f"Found {filename_to_find} at {target_path}")

        # Search for the icon file
        icon_path = find_file(icon_filename, root_search_path)
        if icon_path:
            print(f"Found {icon_filename} at {icon_path}")
        else:
            print(f"{icon_filename} not found. Using default icon.")
            icon_path = target_path  # Use the target file as the icon if the icon file is not found

        # Create the shortcut
        create_shortcut(target_path, icon_path)
    else:
        print(f"{filename_to_find} not found in {root_search_path}")
