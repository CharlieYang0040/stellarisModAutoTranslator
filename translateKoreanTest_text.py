import time
from googletrans import Translator, LANGUAGES
import re
import logging
import sys
import os
import tkinter as tk
from tkinter import filedialog

# 로깅 설정
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Translator instance 생성
translator = Translator()

def translate_text(parts, dest_language):
    translations = []
    for i, part in enumerate(parts):
        if part == "" or part == " ":
            continue
        else:
            translations.append(translator.translate(part, dest=dest_language).text)
            time.sleep(0.5)  # to avoid temporary bans
            logging.info('Translated part %s', i+1)
    return translations

# korean 폴더 내의 모든 .yml 파일 찾기
root = tk.Tk()
root.withdraw()

folder_path = filedialog.askdirectory()
#folder_path = r'C:\Users\jooy1\Documents\WORKDATA\nsc\korean'
yml_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.yml'):
            yml_files.append(os.path.join(root, file))

# korean/translated 경로에 있는 .yml 파일들은 yml_files에서 지우기
translated_folder_path = os.path.join(folder_path, 'translated')
for root, dirs, files in os.walk(translated_folder_path):
    for file in files:
        if file.endswith('.yml'):
            file_path = os.path.join(root, file)
            if file_path in yml_files:
                yml_files.remove(file_path)
                logging.info('Remove existing yml file: %s', file_path)
            # file_path에서 "\translated" 를 지우기
            new_file_path = file_path.replace('\\translated', '')
            if new_file_path in yml_files:
                yml_files.remove(new_file_path)
                logging.info('Remove existing yml file: %s', new_file_path)

for yml_file in yml_files:
    print(yml_file)

# 전체 yml_files 리스트 출력
logging.info('#####Found %s yml files######', len(yml_files))

for yml_file in yml_files:
    file_path = yml_file
    logging.info('Found yml file: %s', file_path)

    # 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        # 분리된 파일 이름 추출
        file_name = os.path.basename(file.name).split('.')[0]
        
        # 로그로 출력
        logging.info('Extracted file name: %s', file_name)
    
    # 따옴표 안의 텍스트 찾기
    quotations = re.findall(r'"([^"]*)"', data)
    logging.info('Found %s quotations to translate', len(quotations))
    
    # 해당 텍스트 번역
    translations = translate_text(quotations, 'ko')
    
    # 번역된 텍스트로 원본 데이터 교체
    for q, t in zip(quotations, translations):
        data = data.replace(f'"{q}"', f'"{t}"')
        
    # 번역된 내용을 새로운 폴더에 쓰기
    translated_folder_path = os.path.join(folder_path, 'translated')
    os.makedirs(translated_folder_path, exist_ok=True)
    translated_file_path = os.path.join(translated_folder_path, os.path.relpath(file_path, folder_path))
    logging.info('Translated_file_path: %s', translated_file_path)
    os.makedirs(os.path.dirname(translated_file_path), exist_ok=True)
    with open(translated_file_path, 'w', encoding='utf-8') as file:
        file.write(data)
        logging.info('Wrote translated text to file: %s', translated_file_path)

    # .txt 확장자를 .yml로 변경
    new_file_path = os.path.splitext(translated_file_path)[0] + '.yml'
    os.rename(translated_file_path, new_file_path)
    logging.info('Renamed file to: %s', new_file_path)