@echo off
chcp 65001 > nul
echo ========================================
echo Установка Meminto
echo ========================================
echo.

REM Проверка Python
echo [1/5] Проверка Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден!
    echo Установите Python 3.11+ с https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Создание виртуального окружения
echo [2/5] Создание виртуального окружения...
if exist venv (
    echo Виртуальное окружение уже существует
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ОШИБКА: Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
    echo Виртуальное окружение создано
)
echo.

REM Активация виртуального окружения
echo [3/5] Активация виртуального окружения...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось активировать виртуальное окружение
    pause
    exit /b 1
)
echo Виртуальное окружение активировано
echo.

REM Обновление pip
echo [4/5] Обновление pip...
python -m pip install --upgrade pip
echo.

REM Установка зависимостей
echo [5/5] Установка зависимостей (это может занять несколько минут)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить зависимости
    echo Попробуйте установить вручную: pip install -r requirements.txt
    pause
    exit /b 1
)
echo.

echo ========================================
echo Установка завершена успешно!
echo ========================================
echo.
echo Следующие шаги:
echo 1. Установите Ollama с https://ollama.com/download
echo 2. Запустите: ollama pull qwen2.5:7b
echo 3. Скопируйте .env.example в .env
echo 4. Добавьте HUGGING_FACE_ACCESS_TOKEN в .env
echo 5. Запустите: python meminto\main.py -f ваш_файл.wav -l russian --use-ollama
echo.
echo Для активации виртуального окружения в будущем:
echo     venv\Scripts\activate
echo.
pause
