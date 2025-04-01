def execute_python_code():
    code = input("Введите код Python для выполнения: ")
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
