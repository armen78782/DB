import os
import git
import time
import itertools
import threading

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

def main_menu():
    print("\033[1;35m┌────────────────────────────────────────────────┐\033[0m")
    print("\033[1;35m│                  Главное меню                 │\033[0m")
    print("\033[1;35m├────────────────────────────────────────────────┤\033[0m")
    print("\033[1;35m│ 1. Поиск по папке SBERBANK                    │\033[0m")
    print("\033[1;35m│ 2. Поиск по базе данных                      │\033[0m")
    print("\033[1;35m│ 3. Поиск в папке 3                           │\033[0m")
    print("\033[1;35m│ 4. Выход                                     │\033[0m")
    print("\033[1;35m└────────────────────────────────────────────────┘\033[0m")
    
    choice = input("\033[1;36mВведите номер действия: \033[0m")
    return choice


if __name__ == "__main__":
    banner = ""
    .:-:.
                                             .-=*#%#=:
                                        :=*%@@@#+:
                                    -+#@@@@@#=.
                                .=#@@@@@@%=
                             :+%@@@@@@@%:                           ...:::::----.
                           =%@@@@@@@@@@=.......:::     .:-=+*#%%@@@@@@@@@@#+=:.
                        .+@@@@@@@@@@@@@@@@@@%*====*#%@@@@@@@@@@@@@@@@%+-.
                       +@@@@@@@@@@@@@@@@*===*%@@@@@@@@@@@@@@@@@@@@@*:
                     -@@@@@@@@@@@@@@#==+#@@@@@@@@@@@@@@@@@@@@@@@@@-
                    #@@@@@@@@@@@@#==#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                   -#%@@@@@@@@@+.+@@@@@@@@@@@@@%%%%@@@@@@@@@@@@@@@:
                      .*@@@@@@#    :=%@@@@@@@@@@@@%#*++=+*%@@@@@@@%
                        *@@@@@#-:     :%@@@@@@@@@@@@@@@@@#+=-=*%@@@#
                        -%####@%##%#+-  *@@@@@@%%@@@@@@@@@@@@@#=:-*@#
                       :+%@@@@@@@#-      #@@@@@@%**%@@@@@@@@@@@@@@*--=
                    .*@@@@@@@@@@@@@#+.   :@@@@@@@@@*=*@@@@@@@@@@@@@@@#-
                   .@@@@@@@@@@@@@@@@#+.   %@@@@+@@@@@#-+@@@@@@@@@@@@@@@@*-
               - .-#@%#@@@@@@@@@@@@@@%=   %@@@@%-%@@@@@*:+@@@@@@@@@@@#+=--:
              -@@@@@@@@@@@@@@@@#@@@@@@@-  %@@@@@%.#@@@@@@+:#@@@@@@*:
               #@@#++:%@#-..:++#*@@@@@%# :@@@@@@@#.%@@@@@@@--%@@@*
                --+= -@#     .#%*@@@@@@  #@@%@@@@@=.@@@@@@@@#:*@@:
           :+####@=.+**+  :=@@++@@@@@*+.*@@@=@@@@@@.-@@@@@@@@@=-@-
          .*+++:.     ::%@@*+*#@@@@@@..#@@@@-#@@@@@# #@@@@@%%@@#:-
         :*%#+.     +@@@+*#+#@@@@@@@**@@@@@@:*@@@@@@-.@@#:    .-*-
        ,.#:     :%=#@@#+%@@@@@@@@@@@@@@@@@ #@@@@@@% *#
                  @@@%+=%@@@@@@@@@@@@@@@@@@# @@@@@@@@:..
                 :*#@%+@@@@@@@@@@@@@@@@@@@@+:@@@#*#@@+
                 :@@#:@@@@@@@@@@@@##***#@@@.+#-     +%
                  =*#=@@@@@@@@@@@@       :+ :        .
                   #%=@@@@@@@@@@@@@@%##**++=-.
                    =##@@@@@@@@@@@@@@@@@@@@@@@%=
                      :-%@@@@@@@@@@@@@@@@@@@@@@@@:
                         :=*%@@@@@@@@%@@@@@@@@@@@%
                                 .:--==--=#@@@@@@@
                             :*%@@@@@@@@@@=#@@@@@#
                            #@@@@#=-:::-=+.%@@@@@:.
                           =@@@@#.      :+@@@@@%-%@+
                           .%@@@@@@%##%@@@@@@%= .#@@%.
                             -*@@@@@@@@@@@%+:     +@@%
                                .--===--.          +@@:
                                                 :..@@:
                                                  #+@@
                                                  :@@-
                                                  .@-
                                                  ..
    """
    
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
            print("\033[1;31mВыход из программы...\033[0m")
            break
        else:
            print("\033[1;31mНекорректный ввод. Попробуйте снова.\033[0m")
