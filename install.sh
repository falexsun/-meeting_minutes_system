#!/bin/bash

echo "========================================"
echo "Установка Meminto"
echo "========================================"
echo

# Проверка Python
echo "[1/5] Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "ОШИБКА: Python3 не найден!"
    echo "Установите Python 3.11+ с https://www.python.org/downloads/"
    exit 1
fi
python3 --version
echo

# Создание виртуального окружения
echo "[2/5] Создание виртуального окружения..."
if [ -d "venv" ]; then
    echo "Виртуальное окружение уже существует"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ОШИБКА: Не удалось создать виртуальное окружение"
        exit 1
    fi
    echo "Виртуальное окружение создано"
fi
echo

# Активация виртуального окружения
echo "[3/5] Активация виртуального окружения..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось активировать виртуальное окружение"
    exit 1
fi
echo "Виртуальное окружение активировано"
echo

# Обновление pip
echo "[4/5] Обновление pip..."
pip install --upgrade pip
echo

# Установка зависимостей
echo "[5/5] Установка зависимостей (это может занять несколько минут)..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось установить зависимости"
    echo "Попробуйте установить вручную: pip install -r requirements.txt"
    exit 1
fi
echo

echo "========================================"
echo "Установка завершена успешно!"
echo "========================================"
echo
echo "Следующие шаги:"
echo "1. Установите Ollama: curl -fsSL https://ollama.com/install.sh | sh"
echo "2. Запустите: ollama pull qwen2.5:7b"
echo "3. Скопируйте: cp .env.example .env"
echo "4. Добавьте HUGGING_FACE_ACCESS_TOKEN в .env"
echo "5. Запустите: python meminto/main.py -f ваш_файл.wav -l russian --use-ollama"
echo
echo "Для активации виртуального окружения в будущем:"
echo "    source venv/bin/activate"
echo
