import time
import os
import re
from distutils.version import LooseVersion

try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Please make sure to install 'requests' and 'tqdm' libraries before running this script.")
    print("You can install them using the following command:")
    print("pip install requests tqdm")
    print("If pip isn't found, try")
    print("pip3 install requests tqdm")
    exit(1)

def get_downloads_folder():
    if 'ANDROID_ROOT' in os.environ:
        # Android
        downloads_folder = os.getcwd()  # Save files in the current directory for Android
    elif os.name == 'posix':
        # Unix/Linux/Mac OS
        downloads_folder = os.path.join(os.path.expanduser("~"), 'Downloads')
    elif os.name == 'nt':
        # Windows
        downloads_folder = os.path.join(os.path.expanduser("~"), 'Downloads')
    else:
        # Fallback to the home directory if the OS is unknown
        downloads_folder = os.path.expanduser("~")
    
    return downloads_folder

def get_user_input():
    while True:
        version_input = input("Enter the desired VirtualBox version in the format xx.xx.xx or xx.xx.xx_BETA(x): ").strip()
        if re.match(r'^\d{1,2}\.\d{1,2}\.\d{1,2}(_BETA\d+)?$', version_input):
            version_parts = version_input.split('_BETA')
            version_numbers = [str(int(segment)) for segment in version_parts[0].split('.')]
            version_number = '.'.join(version_numbers)
            beta_number = version_parts[1] if len(version_parts) > 1 else None
            # Check if version_number is a valid version string
            try:
                LooseVersion(version_number)
            except ValueError:
                print("Invalid version number. Please enter a valid version.")
                continue
            break
        else:
            print("Invalid input. Please enter a valid version number.")
    
    while True:
        choice = input("Enter '1' to download Guest Additions or '2' to download Extension Pack: ")
        if choice in ['1', '2']:
            break
        else:
            print("Invalid choice. Please enter '1' or '2'.")
    
    return version_number, beta_number, choice

def download_file(version, beta, choice, timeout=20):
    downloads_folder = get_downloads_folder()
    if choice == '1':
        if beta:
            file_url = f"https://download.virtualbox.org/virtualbox/{version}_BETA{beta}/VBoxGuestAdditions_{version}_BETA{beta}.iso"
        else:
            file_url = f"https://download.virtualbox.org/virtualbox/{version}/VBoxGuestAdditions_{version}.iso"
        file_name = f"VBoxGuestAdditions_{version}_BETA{beta}.iso"
    elif choice == '2':
        if beta:
            file_url = f"https://download.virtualbox.org/virtualbox/{version}_BETA{beta}/Oracle_VM_VirtualBox_Extension_Pack-{version}_BETA{beta}.vbox-extpack"
        else:
            file_url = f"https://download.virtualbox.org/virtualbox/{version}/Oracle_VM_VirtualBox_Extension_Pack-{version}.vbox-extpack"
        file_name = f"Oracle_VM_VirtualBox_Extension_Pack-{version}_BETA{beta}.vbox-extpack"
    else:
        print("Invalid choice.")
        return False
    
    full_file_path = os.path.join(downloads_folder, file_name)
    
    start_time = time.time()  # Get the start time of the download
    
    while True:
        try:
            response = requests.get(file_url, stream=True, timeout=timeout)
            response.raise_for_status()
            file_size = int(response.headers.get('content-length', 0))
            
            elapsed_time = time.time() - start_time  # Calculate elapsed time
            
            # Check if the file size is less than 8 KB or if the download took too long
            if file_size < 8192 or elapsed_time > timeout:
                print("Download failed. File is corrupted or download took too long.")
                return False
            
            block_size = 1024  # 1 KB
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name)
            
            with open(full_file_path, "wb") as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
            
            progress_bar.close()
            success_message = f"{file_name} downloaded successfully."
            if os.name == 'posix' and 'ANDROID_ROOT' in os.environ:
                success_message += f" It is saved in the current directory: {os.getcwd()}"
            elif os.name == 'posix':
                success_message += f" It is saved in the Downloads folder: {downloads_folder}"
            elif os.name == 'nt':
                success_message += f" It is saved in the Downloads folder: {downloads_folder}"
            else:
                success_message += f" It is saved in the home directory: {downloads_folder}"
            
            print(success_message)
            return True  # Exit the function if download is successful
        except requests.Timeout:
            print("Timeout error: The download took too long. Please try again.")
            return False  # Exit the function if download times out
        except requests.HTTPError as e:
            print(f"HTTP Error: {e}")
            print("You probably entered an invalid version or choice 😂")
            return False
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
            return False

def main():
    while True:
        version, beta, choice = get_user_input()
        download_file(version, beta, choice)
        
        # Ask the user if they want to download another file
        while True:
            try:
                download_another = input("Do you want to download another file? (yes/no): ").strip().lower()
                if download_another in ['yes', 'no']:
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        if download_another == 'no':
            break

if __name__ == "__main__":
    main()
