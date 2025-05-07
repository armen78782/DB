import requests
from termcolor import colored
import os

# ===== КОНФИГУРАЦИЯ =====
REPO_URL = "https://github.com/armen78782/DB/"
REPO_OWNER = REPO_URL.split('/')[3]
REPO_NAME = REPO_URL.split('/')[4]

FOLDERS = {
    '1': {'name': 'OSINT - ПОИСК', 'path': 'probiv'},
    '2': {'name': 'БАЗА SBERBANK', 'path': 'sberbank'},
    '3': {'name': 'Поиск по Telegramm Username', 'path': teleg.py},  # Новый пункт
}

EXTERNAL_SCRIPT_PATH = "./teleg.py"  # путь к скрипту, который будет запускаться

def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print()
    print(colored("========[ HAARROOIN ]========", 'red', attrs=['bold', 'underline']))
    print(colored("        HARROOIN_SOFT", 'cyan', attrs=['bold']))
    print(colored("             by HAARROOIN\n", 'white', attrs=['bold']))

def github_search(folder, keyword):
    print(colored(f"\n[~] Сканирую папку {folder} в GitHub...\n", 'cyan'))
    try:
        api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{folder}"
        response = requests.get(api_url)

        if response.status_code != 200:
            print(colored(f"[!] Ошибка доступа: {response.status_code}", 'red'))
            return 0

        hits = 0
        for item in response.json():
            if item['name'].endswith('.txt'):
                file_url = item['download_url']
                file_content = requests.get(file_url).text

                for line_num, line in enumerate(file_content.split('\n'), 1):
                    if keyword.lower() in line.lower():
                        print(colored(f"\n[+] Файл: {item['path']}", 'green'))
                        print(colored(f" -> Строка {line_num}: {line.strip()}", 'yellow'))
                        hits += 1
        return hits

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

def run_external_script():
    if os.path.isfile(EXTERNAL_SCRIPT_PATH):
        print(colored(f"\n[*] Запуск {EXTERNAL_SCRIPT_PATH}...\n", 'green'))
        os.system(f"python3 {EXTERNAL_SCRIPT_PATH}")
    else:
        print(colored(f"[X] Скрипт не найден по пути: {EXTERNAL_SCRIPT_PATH}", 'red'))

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

        if choice == '3':
            run_external_script()
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