import os
import git
import time
import itertools
import threading
import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
import pandas as pd
from telethon.sync import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import UsernameNotOccupiedError, FloodWaitError
from telethon.tl.types import UserStatusOnline, UserStatusOffline


HEADERS = {"User-Agent": "Mozilla/5.0"}
DATA = []

def animate_text(text, event, color_code="\033[1;34m"):
    for frame in itertools.cycle(['⠇', '⠋', '⠙', '⠸', '⠴', '⠦']):
        if event.is_set():
            break
        print(f"\r{color_code}{text} {frame}\033[0m", end="", flush=True)
        time.sleep(0.1)
    print(f"\r{color_code}{text}... Готово!\033[0m")

def clone_or_update_repo(repo_url, local_path):
    event = threading.Event()
    anim_thread = threading.Thread(target=animate_text, args=("Обработка репозитория", event))
    anim_thread.start()

    try:
        if os.path.exists(local_path):
            repo = git.Repo(local_path)
            repo.remotes.origin.pull()
        else:
            git.Repo.clone_from(repo_url, local_path)
    except Exception as e:
        print(f"\n\033[1;31mОшибка: {e}\033[0m")

    event.set()
    anim_thread.join()

def search_in_txt_files(directory, search_term):
    event = threading.Event()
    anim_thread = threading.Thread(target=animate_text, args=("Поиск", event))
    anim_thread.start()

    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            if search_term in line:
                                results.append(f"\033[1;33mНайдено в {file_path} (строка {line_num}):\033[0m {line.strip()}")
                except Exception as e:
                    print(f"\n\033[1;31mОшибка при чтении {file_path}: {e}\033[0m")

    event.set()
    anim_thread.join()

    print("\n\033[1;36mРезультаты поиска:\033[0m")
    if results:
        for res in results:
            print(res)
    else:
        print("\033[1;31mНичего не найдено.\033[0m")


def scrape_telegram(name_query):
    query = f"site:t.me {name_query}"
    url = f"https://html.duckduckgo.com/html/?q={query}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a", href=True)
    for link in results:
        href = link["href"]
        if "uddg=" in href and "t.me/" in href:
            match = re.search(r'uddg=(.*)', href)
            if match:
                encoded_url = match.group(1)
                decoded_url = urllib.parse.unquote(encoded_url)
                DATA.append({
                    "source": "Telegram",
                    "name": name_query,
                    "email": "",
                    "phone": "",
                    "link": decoded_url
                })

def scrape_github(username):
    url = f"https://github.com/{username}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    name = soup.find("span", class_="p-name")
    bio = soup.find("div", class_="p-note")
    email = soup.find("a", href=lambda x: x and "mailto:" in x)
    DATA.append({"source": "GitHub", "name": name.text.strip() if name else username, "email": email.text.replace("mailto:", "") if email else "", "phone": "", "link": url})

def scrape_vk(name_query):
    query = f"site:vk.com {name_query}"
    url = f"https://duckduckgo.com/html/?q={query}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a", href=True)
    for link in results:
        href = link["href"]
        if "vk.com" in href and "/public" not in href and "/club" not in href:
            DATA.append({"source": "VK", "name": name_query, "email": "", "phone": "", "link": href})

def scrape_avito(search_term):
    url = f"https://www.avito.ru/rossiya?q={search_term}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.find_all("a", href=True)
    for item in items:
        href = item["href"]
        if "/item/" in href:
            full_url = "https://www.avito.ru" + href
            ad = requests.get(full_url, headers=HEADERS)
            ad_soup = BeautifulSoup(ad.text, "lxml")
            text = ad_soup.get_text()
            phones = re.findall(r'\+?\d[\d\s\-\(\)]{8,}\d', text)
            title = ad_soup.find("span", {"itemprop": "name"})
            DATA.append({"source": "Avito", "name": title.text.strip() if title else search_term, "email": "", "phone": phones[0] if phones else "", "link": full_url})
            break

def main_menu():
    print("""\033[1;35m
┌────────────────────────────────────────────────┐
│                 Меню HAARROOIN                 │
├────────────────────────────────────────────────┤
│ 1. Поиск по папке SBERBANK                    │
│ 2. Поиск по базе данных                       │
│ 3. Поиск в папке 3                            │
│ 4. OSINT-поиск от HAARROOIN                   │
│ 5. Выход                                      │
└────────────────────────────────────────────────┘\033[0m""")
    choice = input("\033[1;36mВведите номер действия: \033[0m")
    return choice

def run_osint():
    query = input("\033[1;36mВведите имя или ключевое слово для OSINT-поиска: \033[0m")
    scrape_github(query)
    scrape_vk(query)
    scrape_avito(query)
    scrape_telegram(query) 
    df = pd.DataFrame(DATA)
    print("\n\033[1;36mНайдено:\033[0m")
    print(df)
    df.to_csv("results.csv", index=False)
    print("\033[1;32m\nСохранено в results.csv\033[0m")

if __name__ == "__main__":
    time.sleep(1)
    repo_url = input("\033[1;36mВведите URL репозитория: \033[0m")
    local_repo_path = "repo_clone"
    clone_or_update_repo(repo_url, local_repo_path)
    while True:
        choice = main_menu()
        if choice == '1':
            search_term = input("\n\033[1;36mВведите слово для поиска в папке SBERBANK: \033[0m")
            search_in_txt_files(os.path.join(local_repo_path, "sberbank"), search_term)
        elif choice == '2':
            search_term = input("\n\033[1;36mВведите слово для поиска в базе данных: \033[0m")
            search_in_txt_files(os.path.join(local_repo_path, "probiv"), search_term)
        elif choice == '3':
            search_term = input("\n\033[1;36mВведите слово для поиска в папке 3: \033[0m")
            search_in_txt_files(os.path.join(local_repo_path, "folder3"), search_term)
        elif choice == '4':
            run_osint()
        elif choice == '5':
            print("\033[1;31mВыход из программы...\033[0m")
            break
        else:
            print("\033[1;31mНекорректный ввод. Попробуйте снова.\033[0m""")
