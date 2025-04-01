import socket

def send_packets():
    # Запрашиваем у пользователя количество пакетов, IP-адрес и порт
    target_ip = input("Введите IP-адрес: ")
    target_port = int(input("Введите порт: "))
    packet_count = int(input("Введите количество пакетов для отправки: "))

    # Создаем сокет для отправки данных
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Отправляем пакеты в цикле
    for i in range(packet_count):
        message = f"Пакет {i + 1}".encode()  # Сообщение пакета
        sock.sendto(message, (target_ip, target_port))  # Отправка пакета
        print(f"Пакет {i + 1} отправлен на {target_ip}:{target_port}")

    # Закрываем сокет после отправки всех пакетов
    sock.close()

if __name__ == "__main__":
    send_packets()
 
