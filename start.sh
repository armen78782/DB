#!/data/data/com.termux/files/usr/bin/bash

clear

# Показываем лицо Эллиота как ASCII из .jpg
jp2a --width=70 elliot.jpg

# Пауза
sleep 2

# Запуск Python-софта
python main.py
