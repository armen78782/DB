import pystyle
import requests

GITHUB_REPOS = [
    "https://raw.githubusercontent.com/user/repo/main/data.json",  # Замените на реальные ссылки
    "https://raw.githubusercontent.com/user/repo/main/another_data.json"
]

def getLeakOsinit(query):
    found = False
    for url in GITHUB_REPOS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    if query.lower() in str(entry).lower():
                        pystyle.Write.Print(f"\n[+] Найдено: {entry}\n", pystyle.Colors.green_to_white, interval=0.0001)
                        found = True
            else:
                pystyle.Write.Print(f"[!] Ошибка загрузки данных из {url}\n", pystyle.Colors.red, interval=0.0001)
        except Exception as e:
            pystyle.Write.Print(f"[!] Ошибка: {e}\n", pystyle.Colors.red, interval=0.0001)
    
    if not found:
        pystyle.Write.Print("\n[!] Ничего не найдено\n", pystyle.Colors.blue_to_white, interval=0.0001)

def menu():
    pystyle.Write.Print('''
    MINI DOXX TOOLKIT
    by p1p3tka:
    ______________________________
    |    Пробивает по:           |
    |  [+] Instagram username    |
    |  [+] Telegram username/id  |
    |  [+] Twitter username      |
    |  [+] Facebook              |
    |  [+] Номер телефона        |
    |  [+] Email                 |
    |  [+] VK                    |
    |  [+] и многое другое...    |
    |____________________________|
    ''', pystyle.Colors.blue_to_white, interval=0.0001)

if __name__ == "__main__":
    while True:
    try:
        pystyle.System.Clear()
        query = pystyle.Write.Input("\n[+] Введите запрос для поиска в GitHub: ", pystyle.Colors.blue_to_white, interval=0.0001)
        if query:
            search_github_files(query)
            pystyle.Write.Input("\n[+] Нажмите Enter для продолжения...", pystyle.Colors.blue_to_white, interval=0.0001)
    except KeyboardInterrupt:
        pystyle.Write.Print("\n[-] Выход...", pystyle.Colors.red, interval=0.0001)
        exit()
