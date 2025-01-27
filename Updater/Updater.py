import os
import urllib.request
import json

def get_latest_release_info(repo):
    api_url = f"https://api.github.com/repos/Stari-Div/Python-Utilities/releases/latest" # Remove the brackets
    print(f"Fetching URL: {api_url}")  # Debugging statement
    try:
        with urllib.request.urlopen(api_url) as response:
            if response.status == 200:
                release_info = json.loads(response.read().decode())
                return release_info
            else:
                print(f"Failed to fetch release info: HTTP {response.status}")
    except urllib.error.HTTPError as e:
        print(f"HTTP error occurred: {e.code} - {e.reason}")
        try:
            error_response = e.read().decode()
            print(f"Error details: {error_response}")
        except:
            pass
    except urllib.error.URLError as e:
        print(f"URL error occurred: {e.reason}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def download_file(download_url, download_dir, file_name):
    try:
        # Ensure the download directory exists
        os.makedirs(download_dir, exist_ok=True)
        
        # Download the file
        file_path = os.path.join(download_dir, file_name)
        print(f"Downloading {file_name}...")
        with urllib.request.urlopen(download_url) as response, open(file_path, "wb") as file:
            file.write(response.read())
        print(f"Downloaded {file_name} to {file_path}")
    
    except urllib.error.HTTPError as e:
        print(f"HTTP error occurred: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL error occurred: {e.reason}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # GitHub repository in the format "owner/repo"
    repo = "{Stari-Div}/{Python-Utilities}" # EDIT THIS. Remove the brackets
    
    # Directory to save the downloaded file
    download_dir = "./downloads" # Recommended to leave it as downloads
    
    # Get the latest release info
    release_info = get_latest_release_info(repo) # Boring API stuff
    
    if release_info:
        # Extract the download URL and tag name
        download_url = release_info["zipball_url"]
        tag_name = release_info["tag_name"]
        
        # Create the file name with the tag
        file_name = f"Python-Utilities-{tag_name}.zip" # This adds the update tag after the name of the repo for better identification
        
        # Download the file
        download_file(download_url, download_dir, file_name)
    else:
        print("Failed to retrieve the download URL.")
    # Created by CursedGhoul :) 
