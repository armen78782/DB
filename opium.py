import os
import git
import time
import itertools
import threading

def animate_text(text, event):
    for frame in itertools.cycle(['-', '\', '|', '/']):
        if event.is_set():
            break
        print(f"\r{text} {frame}", end="", flush=True)
        time.sleep(0.1)
    print(f"\r{text}... Готово!")

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
        print(f"Ошибка: {e}")
    
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
                                results.append(f"Найдено в {file_path} (строка {line_num}): {line.strip()}")
                except Exception as e:
                    print(f"Ошибка при чтении {file_path}: {e}")
    
    event.set()
    anim_thread.join()
    
    print("\nРезультаты поиска:")
    if results:
        for res in results:
            print(res)
    else:
        print("Ничего не найдено.")

if __name__ == "__main__":
    repo_url = input("Введите URL репозитория: ")
    local_repo_path = "repo_clone"
    
    print("Запуск программы...")
    time.sleep(1)
    
    clone_or_update_repo(repo_url, local_repo_path)
    
    while True:
        search_term = input("\nВведите слово для поиска (или 'exit' для выхода): ")
        if search_term.lower() == 'exit':
            print("Выход из программы...")
            break
        search_in_txt_files(local_repo_path, search_term)
