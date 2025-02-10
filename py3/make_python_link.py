import os

def make_python3():
    localAppdata = os.getenv('LOCALAPPDATA')
    # C:\Users\Administrator\AppData\Local\Programs\Python\Python313\
    python313 = localAppdata + "\\Programs\\Python\\Python313\\python.exe"
    python311 = localAppdata + "\\Programs\\Python\\Python311\\python.exe"
    python39 = localAppdata + "\\Programs\\Python\\Python39\\python.exe"

    python313_3 = localAppdata + "\\Programs\\Python\\Python313\\python.exe"
    python311_3 = localAppdata + "\\Programs\\Python\\Python311\\python3.exe"
    python39_3 = localAppdata + "\\Programs\\Python\\Python39\\python3.exe"

    if os.path.exists(python313) and not os.path.exists(python313_3):
        os.system(f'mklink "{python313_3}" "{python313}"')
        pass

    if os.path.exists(python311) and not os.path.exists(python311_3):
        os.system(f'mklink "{python311_3}" "{python311}"')
        pass

    if os.path.exists(python39) and not os.path.exists(python39_3):
        os.system(f'mklink "{python39_3}" "{python39}"')
        pass

    pass

make_python3()