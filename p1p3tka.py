import requests
from termcolor import colored
from urllib.parse import urljoin

# ===== КОНФИГУРАЦИЯ ===== (редактируйте эти значения!)
REPO_URL = "https://github.com/armen78782/ВАШ_РЕПОЗИТОРИЙ/"
FOLDERS = {
    '1': {'name': 'OSINT - ПОИСК', 'path': 'sberbank'},
    '2': {'name': 'БАЗА SBERBANK', 'path': 'src'},
}

def github_search(folder, keyword):
    print(colored(f"\n🌐 Сканирую {folder} в GitHub...", 'blue'))
    try:
        # Получаем список файлов через GitHub API
        api_url = f"https://api.github.com/repos/{REPO_URL.split('/')[3]}/{REPO_URL.split('/')[4]}/contents/{folder}"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            print(colored(f"⚠️ Ошибка доступа: {response.status_code}", 'red'))
            return 0
            
        hits = 0
        for item in response.json():
            if item['name'].endswith('.txt'):
                file_url = item['download_url']
                file_content = requests.get(file_url).text
                
                for line_num, line in enumerate(file_content.split('\n'), 1):
                    if keyword.lower() in line.lower():
                        print(colored(f"\n📂 Файл: {item['path']}", 'green'))
                        print(colored(f"📝 Строка {line_num}: {line.strip()}", 'yellow'))
                        hits += 1
        return hits
        
    except Exception as e:
        print(colored(f"💀 Критическая ошибка: {str(e)}", 'red'))
        return 0

def show_menu():
    print(colored("\n=== GITHUB СКАНЕР ===", 'cyan'))
    for num, folder in FOLDERS.items():
        print(f"{num}. {folder['name']}")
    print("0. Выход")
    return input(colored("\nВыберите папку: ", 'white'))

def main():
    global REPO_URL
    REPO_URL = input("Введите URL репозитория (например: https://github.com/user/repo/): ")
    
    while True:
        choice = show_menu()
        
        if choice == '0':
            break
            
        if choice not in FOLDERS:
            print(colored("❌ Неверный выбор!", 'red'))
            continue
            
        folder = FOLDERS[choice]
        keyword = input(colored("🔎 Введите слово для поиска: ", 'white'))
        hits = github_search(folder['path'], keyword)
        print(colored(f"\n🎯 Найдено совпадений: {hits}", 'green'))

if __name__ == "__main__":
    print(colored("\n🕵️‍♂️ GITHUB TEXT SCANNER v3.0 🕵️‍♂️", 'blue'))
    main()