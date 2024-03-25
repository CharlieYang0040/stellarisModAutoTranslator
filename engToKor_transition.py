import os
import tkinter as tk
from tkinter import filedialog
import logging
import shutil

root = tk.Tk()
root.withdraw()

folder_path = filedialog.askdirectory()

files = []
for root, dirs, filenames in os.walk(folder_path):
    for filename in filenames:
        files.append(os.path.join(root, filename))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

for file in files:
    if "_english" in file:
        new_file = file.replace("_english", "_korean")
        shutil.copy(file, new_file)
        logging.info(f"Copied file: {file} -> {new_file}")

files = []
for root, dirs, filenames in os.walk(folder_path):
    for filename in filenames:
        files.append(os.path.join(root, filename))

for file in files:
    if "_korean" in file:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace("l_english:", "l_korean:")
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logging.info(f"Modified file: {file}")
