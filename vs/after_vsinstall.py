import subprocess
import os
import winreg as reg
import json
import shutil




def get_vs_using_vswhere():
    try:
        # Run 'vswhere' to find Visual Studio installation paths
        result = subprocess.run(["coding/vswhere", "-latest", "-property", "installationPath"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

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
        else:
            return False
        
        # Join the paths back into a single string separated by os.pathsep (e.g., ";" for Windows)
        updated_path = os.pathsep.join(current_path)

        # Write the updated PATH back to the registry
        reg.SetValueEx(reg_key, value_name, 0, reg_type, updated_path)

        # Close the registry key
        reg.CloseKey(reg_key)

        # os.system('start C:\\ProgramData\\chocolatey\\bin\\RefreshEnv.cmd')

        print(f"Successfully added '{path}' to the PATH variable.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
    pass

def get_windows_terminal_settings_path():
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        settings_path = os.path.join(local_app_data, "Packages", 
                                     "Microsoft.WindowsTerminal_8wekyb3d8bbwe", 
                                     "LocalState", "settings.json")
        return settings_path
    else:
        return None

def add_git_bash_to_terminal(settings_path):
    if os.path.exists(settings_path):
        # Read the current settings.json file
        with open(settings_path, 'r', encoding='utf-8') as file:
            settings = json.load(file)
        
        # Define the Git Bash profile to add
        git_bash_profile = {
            "guid": "{d99be700-e39f-5380-bbbd-4a7b6ef76e9e}",
            "name": "Git Bash",
            "commandline": "C:\\Program Files\\Git\\bin\\bash.exe -i -l",
            "icon": "C:\\Program Files\\Git\\mingw64\\share\\git\\git-for-windows.ico",
            "hidden": False,
            "startingDirectory": "%USERPROFILE%"
        }
        
        # Check if the Git Bash profile already exists by its name
        profile_exists = False
        if 'profiles' in settings and 'list' in settings['profiles']:
            for profile in settings['profiles']['list']:
                if profile.get("name") == "Git Bash":
                    profile_exists = True
                    break

        # If the profile doesn't exist, add it
        if not profile_exists:
            settings['profiles']['list'].append(git_bash_profile)
            
            # Write the updated settings back to settings.json
            with open(settings_path, 'w', encoding='utf-8') as file:
                json.dump(settings, file, indent=4)
            
            settings['defaultProfile'] = git_bash_profile["guid"]

            print("Git Bash profile has been added to Windows Terminal settings.")
        else:
            print("Git Bash profile already exists.")
    else:
        print(f"settings.json not found at {settings_path}.")

def add_git_bash_vs2022_to_terminal(settings_path):
    if os.path.exists(settings_path):
        # Read the current settings.json file
        with open(settings_path, 'r', encoding='utf-8') as file:
            settings = json.load(file)
        
        # Define the Git Bash profile to add
        git_bash_profile = {
            "guid": "{4e86fa87-bee2-4f95-b161-3366ab2fbde3}",
            "name": "Git Bash VS 2022",
            "commandline": "C:\\Program Files\\Git\\bin\\git-bash_vs2022.cmd",
            "icon": "C:\\Program Files\\Git\\mingw64\\share\\git\\git-for-windows.ico",
            "hidden": False,
            "startingDirectory": "%USERPROFILE%"
        }
        
        # Check if the Git Bash profile already exists by its name
        profile_exists = False
        if 'profiles' in settings and 'list' in settings['profiles']:
            for profile in settings['profiles']['list']:
                if profile.get("name") == "Git Bash VS 2022":
                    profile_exists = True
                    break

        # If the profile doesn't exist, add it
        if not profile_exists:
            settings['profiles']['list'].append(git_bash_profile)
            
            # Write the updated settings back to settings.json
            with open(settings_path, 'w', encoding='utf-8') as file:
                json.dump(settings, file, indent=4)
            
            # settings['defaultProfile'] = git_bash_profile["guid"]

            print("Git Bash VS 2022 profile has been added to Windows Terminal settings.")
        else:
            print("Git Bash VS 2022 profile already exists.")
    else:
        print(f"settings.json not found at {settings_path}.")

def add_elevate_default(settings_path):
    if os.path.exists(settings_path):
        # Read the current settings.json file
        with open(settings_path, 'r', encoding='utf-8') as file:
            settings = json.load(file)
        
        # Check if "defaults" exists in the profiles section
        if 'profiles' in settings:
            if 'defaults' not in settings['profiles']:
                # Add the "defaults": { "elevate": true } block if it does not exist
                settings['profiles']['defaults'] = {
                    "elevate": True
                }
                print('Added "defaults": { "elevate": true } to settings.json.')
            else:
                # Check if the "elevate" field exists and is set to True
                if settings['profiles']['defaults'].get('elevate', False) is not True:
                    settings['profiles']['defaults']['elevate'] = True
                    print('Updated "elevate" to true in the defaults section.')
                else:
                    print('"elevate" is already set to true.')
            
            # Write the updated settings back to settings.json
            with open(settings_path, 'w', encoding='utf-8') as file:
                json.dump(settings, file, indent=4)

        else:
            print('"profiles" section not found in settings.json.')
    else:
        print(f"settings.json not found at {settings_path}.")

def add_git_bash_vs2022_to_terminal_start(settings_path):
    shutil.copyfile("coding/git-bash_vs2022.cmd", "C:\\Program Files\\Git\\bin\\git-bash_vs2022.cmd")
    add_git_bash_vs2022_to_terminal(settings_path)
    pass

def start():
    vs_path = get_vs_using_vswhere()
    if not vs_path:
        print("Visual Studio installation not found using vswhere.")
        return
    
    settings_path = get_windows_terminal_settings_path()
    if settings_path and os.path.exists(settings_path):
        print(f"Windows Terminal settings.json is located at: {settings_path}")
        add_git_bash_to_terminal(settings_path)
        add_elevate_default(settings_path)
        add_git_bash_vs2022_to_terminal_start(settings_path)
    else:
        print("Windows Terminal settings.json not found.")
    
    need_restart = add_env_path(vs_path + "\\Common7\\Tools")
    if need_restart:
        os.system("taskkill /f /im explorer.exe && start explorer.exe")

start()

# Example: Get the path to Windows Terminal settings.json
