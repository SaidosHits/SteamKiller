import requests
import os
import re
import time
import zipfile
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_logo():
    purple = Fore.MAGENTA  # Purple color
    logo_lines = [
    
        "      _____ _                        _   ___ _ _           ",
        "     /  ___| |                      | | / (_) | |          ",
        "     \\ `--.| |_ ___  __ _ _ __ ___  | |/ / _| | | ___ _ __ ",
        "      `--. \\ __/ _ \\/ _` | '_ ` _ \\ |    \\| | | |/ _ \\ '__|",
        "     /\\__/ / ||  __/ (_| | | | | | || |\\  \\ | | |  __/ |   ",
        "     \\____/ \\__\\___|\\__,_|_| |_| |_|\\_| \\_/_|_|_|\\___|_|   "
        "                                                                  ",
        "                        by @SaidosHits                             ",
    ]
    for line in logo_lines:
        print(purple + line + Style.RESET_ALL)
        time.sleep(0.05)

def get_filename_from_cd(cd):
    """Extract filename from Content-Disposition header."""
    if not cd:
        return None
    fname = re.findall('filename="?([^"]+)"?', cd)
    return fname[0] if fname else None

def main():
    print_logo()

    app_id = input(f"{Fore.CYAN}Enter your AppId: ").strip()

    if not app_id:
        print(f"{Fore.RED}[!] appId cannot be empty.")
        return

    api_url = "https://cysaw.org/api.php"
    payload = {"appId": app_id}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        # Step 1: POST request
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "success" or not data.get("dirName"):
            print(f"{Fore.RED}[-] API error or missing dirName.")
            return

        dir_name = data["dirName"]
        download_url = f"https://cysaw.org/d.php?token={dir_name}"

        print(f"{Fore.GREEN}[+] Downloading... Please wait.")

        # Step 2: Download the file
        download_response = requests.get(download_url, headers=headers)
        download_response.raise_for_status()

        # Step 3: Get filename
        cd_header = download_response.headers.get("Content-Disposition")
        filename = get_filename_from_cd(cd_header) or f"{dir_name}.zip"

        # Step 4: Ensure the 'result' directory exists
        result_dir = os.path.join(os.getcwd(), "result")
        os.makedirs(result_dir, exist_ok=True)

        file_path = os.path.join(result_dir, filename)

        # Step 5: Save the ZIP file
        with open(file_path, "wb") as f:
            f.write(download_response.content)

        print(f"{Fore.GREEN}[✓] Download completed!")

        # Step 6: Extract the ZIP file to folder with same name (without .zip)
        extract_folder = os.path.join(result_dir, os.path.splitext(filename)[0])
        os.makedirs(extract_folder, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        print(f"{Fore.GREEN}[✓] Extracted files to: {extract_folder}")

        # Step 7: Remove the zip file
        os.remove(file_path)


        # Step 8: Remove readme.txt if exists
        readme_path = os.path.join(extract_folder, "readme.txt")
        if os.path.isfile(readme_path):
            os.remove(readme_path)
            

    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")

if __name__ == "__main__":
    main()
