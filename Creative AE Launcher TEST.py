import threading
import os
import urllib.request
import zipfile
import subprocess
import sys

# Set the base directory and the GitHub URL for the repository ZIP
base_dir = os.path.dirname(os.path.abspath(__file__))
repo_url = "https://github.com/AinzOoalGown1356/AECreative_UI/archive/refs/heads/main.zip"
zip_path = os.path.join(base_dir, "AECreative_UI.zip")
extract_dir = os.path.join(base_dir, "AECreative_UI-main")

# Function to download and extract the repository if it doesn't exist
def download_and_extract_repo():
    if not os.path.exists(extract_dir):
        print(f"Downloading repository to {zip_path}...")
        try:
            # Download the ZIP file
            urllib.request.urlretrieve(repo_url, zip_path)
            print("Repository downloaded successfully.")

            # Extract the ZIP file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(base_dir)
            print(f"Repository extracted to {extract_dir}.")

            # Remove the ZIP file after extraction
            os.remove(zip_path)
        except Exception as e:
            print(f"Failed to download and extract the repository: {e}")
            sys.exit(1)
    else:
        print("Repository already exists. Proceeding to execute...")

# Download and extract the repository if needed
download_and_extract_repo()

# Path to the UI script within the extracted repository
ui_script_path = os.path.join(extract_dir, "Ace AE Creative.py")

# Function to run the GUI in a separate thread
def run_gui():
    try:
        subprocess.run([sys.executable, ui_script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute the UI: {e}")

# Start the GUI in a separate thread
gui_thread = threading.Thread(target=run_gui)
gui_thread.start()

# The GUI is now running in the background
# Your main script can continue here, without interfering with the computer vision