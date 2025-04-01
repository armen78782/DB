def execute_python_code():
    code = import socket
import time

# Запрос IP-адреса и порта
target_ip = input("Введите IP-адрес назначения: ")  # Вводим IP
target_port = int(input("Введите порт назначения: "))  # Вводим порт

# Создаем сокет для отправки данных
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Сообщение для отправки
message = b"Привет, это тестовый пакет"

# Бесконечный цикл для отправки пакетов
while True:
    # Отправляем пакет
    sock.sendto(message, (target_ip, target_port))
    print(f"Пакет отправлен на {target_ip}:{target_port}")
    
    # Добавим паузу в 1 секунду, чтобы не перегружать сеть
    time.sleep(1)  # 1 секунда

    try:
        exec(code)
    except Exception as e:
        print(f"Произошла ошибка при выполнении кода: {e}")

def menu():
    print("Выберите опцию:")
    print("1. Функция 1")
    print("2. Функция 2")
    print("3. Выполнить Python код")
    choice = input("Введите номер опции: ")

    if choice == '1':
        function_1()
    elif choice == '2':
        function_2()
    elif choice == '3':
        execute_python_code()
    else:
        print("Неверный выбор. Попробуйте снова.")
        menu()

# Запускаем меню
menu()
