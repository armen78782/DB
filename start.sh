#!/data/data/com.termux/files/usr/bin/bash

clear

# Открываем JPG-файл во внешней галерее
am start -a android.intent.action.VIEW -d file:///data/data/com.termux/files/home/your-project/elliot.jpg -t image/jpeg

# Небольшая пауза, чтобы пользователь успел увидеть картинку
sleep 2

# Запуск Python-программы
python p1p3tka.py
