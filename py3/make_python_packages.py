import os

os.system("python3 -m pip install PyGithub")
os.system("python3 -m pip install clint")
os.system("python3 -m pip install pycryptodome")
os.system("python3 -m pip install tqdm")
os.system("python3 -m pip install rarfile")

os.system("python3 -m pip uninstall -y pipywin32")
os.system("python3 -m pip uninstall -y pywin32")
os.system("python3 -m pip install pywin32")