import os
import urllib.request
import zipfile
import winreg as reg
from github import Github

def get_rebs_latest_asset():
    g = Github()
    repo = g.get_repo("osdeverr/rebs")

    release = repo.get_latest_release()
    for asset in release.get_assets():
        if "Windows" in asset.name:
            
            rebs_result = {}
            rebs_result["tag_name"] = release.tag_name
            rebs_result["asset_name"] = asset.name
            rebs_result["browser_download_url"] = asset.browser_download_url

            g.close()

            return rebs_result
            
    return None

def get_rebt_latest_asset():
    g = Github()
    repo = g.get_repo("osdeverr/re-build-tools")

    release = repo.get_latest_release()
    for asset in release.get_assets():
        if "vsix" in asset.name:    

            rebs_result = {}
            rebs_result["tag_name"] = release.tag_name
            rebs_result["asset_name"] = asset.name
            rebs_result["browser_download_url"] = asset.browser_download_url

            g.close()

            return rebs_result
            
    return None


# Define the registry key and value for PATH (User or System)
software_path = "C:\\Software"
cache_path = ".\\cache"

def test_path_exists_in(path: str, path_list: list[str]):
    prepared_path_list = []
    for existing_path in path_list:
        prepared_path_list.append(existing_path.lower().rstrip('\\/ '))
        pass

    prepared_path = path.lower().rstrip('\\/ ')
    return prepared_path in prepared_path_list

def add_env_path(path: str):
    key = reg.HKEY_CURRENT_USER  # For the current user (use HKEY_LOCAL_MACHINE for system-wide)
    reg_path = "Environment"   # Location where PATH is stored
    value_name = "Path"         # The name of the PATH variable in the registry

    path = path.replace('/', "\\")

    try:
        # Open the registry key where the PATH variable is stored
        reg_key = reg.OpenKey(key, reg_path, 0, reg.KEY_READ | reg.KEY_WRITE)

        # Get the current PATH variable value (it could be a string or a list of strings)
        current_path, reg_type = reg.QueryValueEx(reg_key, value_name)
        # print(f"Prev PATH is: {current_path}")

        # If it's a string, convert it to a list for easier modification
        if isinstance(current_path, str):
            current_path = current_path.split(os.pathsep)
            if current_path[-1] == '':
                current_path.pop()

        # print(f"current PATH is: {current_path}")

        # Avoid adding the new path if it's already present
        if not test_path_exists_in(path, current_path):
            current_path.append(path)
        
        # Join the paths back into a single string separated by os.pathsep (e.g., ";" for Windows)
        updated_path = os.pathsep.join(current_path)

        # Write the updated PATH back to the registry
        reg.SetValueEx(reg_key, value_name, 0, reg_type, updated_path)

        # Close the registry key
        reg.CloseKey(reg_key)

        # os.system('start C:\\ProgramData\\chocolatey\\bin\\RefreshEnv.cmd')

        print(f"Successfully added '{path}' to the PATH variable.")

    except Exception as e:
        print(f"Error: {e}")
    pass

def load_vscode_extensions():
    os.system("code --install-extension ms-python.python")
    os.system("code --install-extension ms-vscode.cpptools-extension-pack")
    os.system("code --install-extension llvm-vs-code-extensions.vscode-clangd")
    pass

def approve_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def approve_software_path():
    approve_path(software_path)


def install_rebs():
    approve_software_path()

    asset = get_rebs_latest_asset()

    download_path = cache_path + "\\" + asset["asset_name"]
    rebs_path = software_path + f"\\rebs_{asset['tag_name']}"

    os.makedirs(cache_path, exist_ok=True)
    os.makedirs(rebs_path, exist_ok=True)

    print(f"Downloading: {asset['browser_download_url']}")
    result = urllib.request.urlretrieve(asset["browser_download_url"], download_path)
    success = False
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(rebs_path)
        print(f'rebs { asset["tag_name"] } successfully installed to { rebs_path }')
        success = True

    if not success:
        print(f"Rebs installation failed")
        return

    add_env_path(rebs_path)

    pass

def install_rebs_extension():
    asset = get_rebt_latest_asset()

    print(f"Downloading: {asset['browser_download_url']}")

    download_path = cache_path + "\\" + asset["asset_name"]
    os.makedirs(cache_path, exist_ok=True)

    result = urllib.request.urlretrieve(asset["browser_download_url"], download_path)
    os.system(f'code --install-extension "{ download_path }"')
    print(f"{ asset['asset_name'] } successfully installed")

    pass


load_vscode_extensions()
install_rebs()
install_rebs_extension()

# os.system("rundll32.exe user32.dll,UpdatePerUserSystemParameters")
# Refresh PATH
os.system("taskkill /f /im explorer.exe && start explorer.exe")