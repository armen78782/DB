import requests
from termcolor import colored
import os
import csv
from openpyxl import load_workbook
import io

# ===== КОНФИГУРАЦИЯ =====
REPO_URL = "https://github.com/armen78782/DB/"
REPO_OWNER = REPO_URL.split('/')[3]
REPO_NAME = REPO_URL.split('/')[4]

FOLDERS = {
    '1': {'name': 'OSINT - ПОИСК', 'path': 'probiv'},
    '2': {'name': 'БАЗА SBERBANK', 'path': 'sberbank'},
    '3': {'name': 'Поиск по IP', 'path': 'teleg.py'},  # Новый пункт
    '4': {'name': 'Поиск по Утечкам', 'path': 'utechk.py'},  # Новый пункт для скрипта
}

def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print()
    print(colored("========[ HAARROOIN ]========", 'red', attrs=['bold', 'underline']))
    print(colored("        HARROOIN_SOFT", 'cyan', attrs=['bold']))
    print(colored("             by HAARROOIN\n", 'white', attrs=['bold']))

def read_txt_file(file_content, keyword):
    hits = 0
    for line_num, line in enumerate(file_content.split('\n'), 1):
        if keyword.lower() in line.lower():
            print(colored(f"\n[HARROOIN SOFT]", 'green', attrs=['bold']))
            print(colored(f"[•] Строка {line_num}: ", 'yellow') + colored(line.strip(), 'white', attrs=['bold', 'underline']))
            hits += 1
    return hits

def read_csv_file(file_content, keyword):
    hits = 0
    csv_reader = csv.reader(io.StringIO(file_content))
    for line_num, row in enumerate(csv_reader, 1):
        for cell in row:
            if keyword.lower() in cell.lower():
                print(colored(f"\n[HARROOIN SOFT]", 'green', attrs=['bold']))
                print(colored(f"[+] Строка {line_num}: ", 'yellow') + colored(cell.strip(), 'white', attrs=['bold', 'underline']))
                hits += 1
    return hits

def read_xlsx_file(file_content, keyword):
    hits = 0
    workbook = load_workbook(filename=io.BytesIO(file_content))
    for sheet in workbook.sheetnames:
        worksheet = workbook[sheet]
        for row in worksheet.iter_rows(values_only=True):
            for cell in row:
                if cell and keyword.lower() in str(cell).lower():
                    print(colored(f"\n[HARROOIN SOFT] Найдено совпадение в листе '{sheet}'!", 'green', attrs=['bold']))
                    print(colored(f"[+] Значение: ", 'yellow') + colored(str(cell).strip(), 'white', attrs=['bold', 'underline']))
                    hits += 1
    return hits

def github_search(folder, keyword):
    print(colored(f"\n[~] Сканирую папку {folder}...\n", 'cyan'))
    try:
        api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{folder}"
        response = requests.get(api_url)

        if response.status_code != 200:
            print(colored(f"[!] Ошибка доступа: {response.status_code}", 'red'))
            return 0

        hits = 0
        for item in response.json():
            file_url = item['download_url']
            if item['name'].endswith('.txt'):
                file_content = requests.get(file_url).text
                hits += read_txt_file(file_content, keyword)
            elif item['name'].endswith('.csv'):
                file_content = requests.get(file_url).text
                hits += read_csv_file(file_content, keyword)
            elif item['name'].endswith('.xlsx'):
                file_content = requests.get(file_url).content
                hits += read_xlsx_file(file_content, keyword)

        if hits == 0:
            print(colored("\n[-] Нет совпадений в файлах.", 'red'))

    except Exception as e:
        print(colored(f"[X] Критическая ошибка: {str(e)}", 'red'))
        return 0

def show_menu():
    print(colored("=" * 45, 'red'))
    for num, folder in FOLDERS.items():
        print(colored(f"[{num}] {folder['name']}", 'white'))
    print(colored("[0] ВЫХОД", 'white'))
    print(colored("=" * 45, 'red'))
    return input(colored(">>> ВЫБЕРИТЕ ПАПКУ: ", 'cyan'))

def main():
    banner()
    while True:
        choice = show_menu()

        if choice == '0':
            print(colored("\n[!] Выход...\n", 'red'))
            break

        if choice not in FOLDERS:
            print(colored("[X] Неверный выбор!", 'red'))
            continue

        # Обработка выбора для запуска Python-скрипта
        if choice in ['3', '4']:
            script_path = FOLDERS[choice]['path']
            if os.path.isfile(script_path):
                print(colored(f"\n[*] Запуск {script_path}...\n", 'green'))
                os.system(f"python3 {script_path}")
            else:
                print(colored(f"[X] Скрипт не найден: {script_path}", 'red'))
            input(colored("\nНажмите Enter для продолжения...", 'magenta'))
            banner()
            continue

        folder = FOLDERS[choice]
        keyword = input(colored(">>> Введите слово для поиска: ", 'cyan'))
        hits = github_search(folder['path'], keyword)
        print(colored(f"\n[*] Найдено совпадений: {hits}", 'green'))
        input(colored("\nНажмите Enter для продолжения...", 'magenta'))
        banner()

if __name__ == "__main__":
    main()
