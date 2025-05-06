import os
from termcolor import colored
import sys

def search_in_files(directory, keyword):
    hits = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if keyword.lower() in line.lower():
                                print(colored(f"🩸 {path}", 'red'))
                                print(colored(f"📌 Строка {line_num}: {line.strip()}", 'yellow'))
                                hits += 1
                except Exception as e:
                    print(colored(f"☠️ Ошибка в {path}: {str(e)}", 'magenta'))
    return hits

def show_menu():
    print(colored("\n🖥️ ТЕРМИНАЛЬНЫЙ ИНТЕРФЕЙС АКТИВИРОВАН", 'cyan'))
    print(colored("1. Сканировать текущую директорию", 'green'))
    print(colored("2. Выбрать конкретную папку", 'green'))
    print(colored("3. Выход в хаос", 'red'))
    return input(colored("ВВОД КОМАНДЫ: ", 'white'))

def main():
    while True:
        choice = show_menu()
        
        if choice == '1':
            target_dir = '.'
        elif choice == '2':
            dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
            print(colored("\n📂 ДОСТУПНЫЕ ПАПКИ:", 'blue'))
            for idx, d in enumerate(dirs, 1):
                print(f"{idx}. {d}")
            dir_choice = int(input(colored("ВЫБЕРИТЕ НОМЕР ПАПКИ: ", 'white'))) - 1
            target_dir = dirs[dir_choice]
        elif choice == '3':
            print(colored("🌀 СИСТЕМА САМОУНИЧТОЖЕНИЯ АКТИВИРОВАНА", 'red'))
            sys.exit()
        
        keyword = input(colored("\n🔎 ВВЕДИТЕ КЛЮЧЕВОЕ СЛОВО/ФРАЗУ: ", 'white'))
        total_hits = search_in_files(target_dir, keyword)
        print(colored(f"\n☣️ НАЙДЕНО СОВПАДЕНИЙ: {total_hits}", 'cyan'))

if __name__ == "__main__":
    print(colored("⚡ ZORG-MASTER DATA HARVESTER v9.66 ⚡", 'white', 'on_red'))
    main()