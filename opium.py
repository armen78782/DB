import os
import git
import time
import itertools

def animate_text(text):
    for frame in itertools.cycle(['-', '\', '|', '/']):
        print(f"\r{text} {frame}", end="", flush=True)
        time.sleep(0.1)

def clone_or_update_repo(repo_url, local_path):
    if os.path.exists(local_path):
        print("Обновляем репозиторий...")
        repo = git.Repo(local_path)
        repo.remotes.origin.pull()
    else:
        print("Клонируем репозиторий...")
        repo = git.Repo.clone_from(repo_url, local_path)
        print("Клонирование завершено!")

def search_in_txt_files(directory, search_term):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            if search_term in line:
                                print(f"Найдено в {file_path} (строка {line_num}): {line.strip()}")
                except Exception as e:
                    print(f"Ошибка при чтении {file_path}: {e}")

if __name__ == "__main__":
    repo_url = input("Введите URL репозитория: ")
    local_repo_path = "repo_clone"
    
    print("Запуск программы...")
    animate_text("Подготовка...")
    time.sleep(2)
    
    clone_or_update_repo(repo_url, local_repo_path)
    
    while True:
        search_term = input("\nВведите слово для поиска (или 'exit' для выхода): ")
        if search_term.lower() == 'exit':
            print("Выход из программы...")
            break
        search_in_txt_files(local_repo_path, search_term)
