import os
from datetime import datetime
from telethon import TelegramClient, functions, types
from telethon.tl.types import User, InputPrivacyKeyPhoneNumber, InputPrivacyValueDisallowAll

api_id = '23319571'  # Получить на my.telegram.org
api_hash = 'e9cade797f8a9b29432cc955438057a2'
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    target = input("[🌑] Введите username/id цели: ")
    user = await client.get_entity(target)
    
    if not isinstance(user, User):
        print("[💀] Цель не является пользователем!")
        return

    # Основная информация
    print(f"\n[🔮] ОСНОВНЫЕ ДАННЫЕ:")
    print(f"ID: {user.id}")
    print(f"Username: @{user.username}")
    print(f"Имя: {user.first_name}")
    print(f"Фамилия: {user.last_name}")
    print(f"Био: {user.about}")
    print(f"Премиум: {user.premium}")
    print(f"Бот: {user.bot}")
    print(f"Фейк: {user.fake}")
    print(f"Скам: {user.scam}")
    print(f"Последний онлайн: {user.status.was_online}")

    # Анализ активности
    print(f"\n[📈] АКТИВНОСТЬ:")
    try:
        async for msg in client.iter_messages(user, limit=5):
            print(f"{msg.date.strftime('%Y-%m-%d %H:%M')}: {msg.text[:50]}...")
    except Exception as e:
        print(f"Не удалось получить сообщения: {str(e)}")

    # Социальный граф
    print(f"\n[🕸️] СОЦИАЛЬНЫЕ СВЯЗИ:")
    common_chats = await client.get_common_chats(user.id)
    print(f"Общие чаты ({len(common_chats)}):")
    for chat in common_chats[:3]:
        print(f"- {chat.title} (ID: {chat.id})")

    # Скачивание медиа
    print(f"\n[📷] МЕДИА:")
    media_path = f"/sdcard/Telegram_Data/{user.id}"
    os.makedirs(media_path, exist_ok=True)
    try:
        async for msg in client.iter_messages(user, limit=3, filter=types.InputMessagesFilterPhotoVideo):
            await client.download_media(msg, media_path)
            print(f"Скачано: {msg.id}")
    except:
        print("Нет доступа к медиа")

    # Защита приватности (ваша)
    await client(functions.account.UpdatePrivacyRequest(
        key=InputPrivacyKeyPhoneNumber,
        rules=[InputPrivacyValueDisallowAll()]
    ))

with client:
    client.loop.run_until_complete(main())