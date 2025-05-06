import requests
from termcolor import colored
from urllib.parse import urljoin
import os

# ===== КОНФИГУРАЦИЯ =====
REPO_URL = "https://github.com/armen78782/DB/"
FOLDERS = {
    '1': {'name': 'OSINT - ПОИСК', 'path': 'probiv'},
    '2': {'name': 'БАЗА SBERBANK', 'path': 'sberbank'},
}

def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(colored(r"""
██╗  ██╗ █████╗  █████╗ ██████╗ ██████╗  ██████╗ ██╗███╗   ██╗
██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██║████╗  ██║
███████║███████║███████║██████╔╝██████╔╝██║   ██║██║██╔██╗ ██║
██╔══██║██╔══██║██╔══██║██╔═══╝ ██╔═══╝ ██║   ██║██║██║╚██╗██║
██║  ██║██║  ██║██║  ██║██║     ██║     ╚██████╔╝██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═════╝ ╚═╝╚═╝  ╚═══╝
        HARROIN_SOFT
    """, 'red'))
    print(colored("               by HAARROIN\n", 'white'))

def github_search(folder, keyword):
    print(colored(f"\n[~] Сканирую папку {folder} в GitHub...\n", 'cyan'))
    try:
        api_url = f"https://api.github.com/repos/{REPO_URL.split('/')[3]}/{REPO_URL.split('/')[4]}/contents/{folder}"
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

def main():
    global REPO_URL
    banner()
    REPO_URL = input(colored(">>> Введите URL репозитория: ", 'cyan'))

    while True:
        choice = show_menu()

        if choice == '0':
            print(colored("\n[!] Выход...\n", 'red'))
            break

        if choice not in FOLDERS:
            print(colored("[X] Неверный выбор!", 'red'))
            continue

        folder = FOLDERS[choice]
        keyword = input(colored(">>> Введите слово для поиска: ", 'cyan'))
        hits = github_search(folder['path'], keyword)
        print(colored(f"\n[*] Найдено совпадений: {hits}", 'green'))
        input(colored("\nНажмите Enter для продолжения...", 'magenta'))
        banner()

if __name__ == "__main__":
    main()