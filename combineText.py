import tkinter as tk
from tkinter import filedialog

def combine_text_files(file_paths):
    file_paths = sorted(file_paths, key=lambda x: int(''.join(filter(str.isdigit, x))))
    merged_file = file_paths[0].replace('_output_', '_combined_')
    with open(merged_file, 'w', encoding='utf-8') as outfile:
        for file_path in file_paths:
            filename = file_path
            with open(filename, encoding='utf-8') as infile:
                contents = infile.read()
                outfile.write(contents)
                print(f"Combined files into {merged_file}.")

# Usage example
root = tk.Tk()
root.withdraw()

folder_path = filedialog.askopenfilenames()
combine_text_files(folder_path)