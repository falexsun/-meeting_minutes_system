import os
from huggingface_hub import whoami
from dotenv import load_dotenv

# Загружаем токен из .env файла
load_dotenv()
token = os.getenv("HUGGING_FACE_ACCESS_TOKEN")

if not token:
    print("❌ Токен не найден! Создайте .env файл с HUGGING_FACE_ACCESS_TOKEN")
    exit(1)

try:
    user_info = whoami(token=token)
    print("✅ Токен рабочий!")
    print("Информация о пользователе:", user_info)
except Exception as e:
    print("❌ Токен недействителен или произошла ошибка:", e)