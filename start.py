import os
import asyncio
import subprocess

def choco_install():
    result = os.system("choco --version")
    if result != 0:
        os.system('winget install "Chocolatey.Chocolatey"')

def choco_check():
    result = os.system("choco --version")
    if result != 0:
        os.system("taskkill /f /im explorer.exe >nul && start explorer.exe >nul")
        print("Choco is not ready. code:", result)
        print("Restart your console and launch script again to continue installation")
        return False

    return True

def winget_check():
    result = os.system("winget --version")
    if result != 0:
        print('winget is not ready, you can download msix package via command:')
        print('powershell Invoke-WebRequest -Uri "https://github.com/microsoft/winget-cli/releases/download/v1.9.25180/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle" -OutFile ".\winget.msixbundle"')
        return False
    
    return True

async def vs_pass():
    vsinstall = subprocess.Popen('cmd /c "vs\\vsinstall.bat"', creationflags=subprocess.CREATE_NEW_CONSOLE)
    await asyncio.to_thread(vsinstall.wait)

    after_vsinstall = subprocess.Popen('python3 "vs\\after_vsinstall.py"', creationflags=subprocess.CREATE_NEW_CONSOLE)
    await asyncio.to_thread(after_vsinstall.wait)

async def subtools_pass():
    def commands():
        os.system('choco install llvm -y')
        os.system('choco install cmake -y')
        os.system('choco install nodejs -y')

    await asyncio.to_thread(commands)

def check_wt():
    result = os.system("winget --version")
    pass

def start():
    if not winget_check():
        return

    choco_install()
    if not choco_check():
        return
    
    os.system('python3 "py3\\make_python_link.py"')
    os.system('python3 "py3\\make_python_packages.py"')

    os.system('winget install "Microsoft.WindowsTerminal"')
    os.system('choco install vscode -y')
    os.system('choco install git -y')

    async def do_gather():
        await asyncio.gather(subtools_pass(), vs_pass())

    asyncio.run(do_gather())

    os.system('python3 "rebs\\install_rebs.py"')

start()