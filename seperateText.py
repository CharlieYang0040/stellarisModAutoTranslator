import tkinter as tk
from tkinter import filedialog

def split_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    num_lines = len(lines)
    num_files = num_lines // 300 + 1

    for i in range(num_files):
        start = i * 300
        end = min((i + 1) * 300, num_lines)
        file_name = file_path.replace('.yml', f'_output_{i}.yml')

        with open(file_name, 'w', encoding='utf-8') as output_file:
            output_file.writelines(lines[start:end])

        print(f"Created {file_name} with {end - start} lines.")

# Usage example
root = tk.Tk()
root.withdraw()

folder_path = filedialog.askopenfilename()
split_text_file(folder_path)