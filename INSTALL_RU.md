# Упрощенная установка Meminto

## Вариант 1: Через pip (рекомендуется для начинающих)

### Windows (PowerShell или CMD)

```powershell
# 1. Создайте виртуальное окружение
python -m venv venv

# 2. Активируйте виртуальное окружение
.\venv\Scripts\activate

# 3. Обновите pip
python -m pip install --upgrade pip

# 4. Установите зависимости
pip install -r requirements.txt

# 5. Проверьте установку
python -c "import torch; print('PyTorch:', torch.__version__)"
```

### Linux / macOS

```bash
# 1. Создайте виртуальное окружение
python3 -m venv venv

# 2. Активируйте виртуальное окружение
source venv/bin/activate

# 3. Обновите pip
pip install --upgrade pip

# 4. Установите зависимости
pip install -r requirements.txt

# 5. Проверьте установку
python -c "import torch; print('PyTorch:', torch.__version__)"
```

## Вариант 2: Через Poetry (для опытных пользователей)

### Установка Poetry

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**Linux / macOS:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### После установки Poetry

```bash
# Добавьте Poetry в PATH и перезапустите терминал

# Установите зависимости
poetry install

# Активируйте окружение
poetry shell
```

## После установки

### 1. Установите Ollama

**Windows:**
- Скачайте с https://ollama.com/download
- Установите и запустите
- Откройте CMD/PowerShell:
  ```powershell
  ollama pull qwen2.5:7b
  ```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b
```

### 2. Настройте .env

```bash
# Скопируйте пример
copy .env.example .env    # Windows
# или
cp .env.example .env      # Linux/macOS

# Отредактируйте .env и добавьте:
# HUGGING_FACE_ACCESS_TOKEN=ваш_токен
```

### 3. Запустите обработку

```bash
# С активированным виртуальным окружением
python meminto/main.py -f ваш_файл.wav -l russian --use-ollama
```

## Проверка установки

Выполните эти команды для проверки:

```bash
# Проверка Python
python --version
# Должно быть >= 3.11

# Проверка PyTorch
python -c "import torch; print('PyTorch:', torch.__version__)"

# Проверка CUDA (опционально, для GPU)
python -c "import torch; print('CUDA доступна:', torch.cuda.is_available())"

# Проверка Ollama
curl http://localhost:11434/api/tags
```

## Типичные проблемы

### 1. Ошибка "No module named 'torch'"

```bash
# Переустановите PyTorch
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Ошибка при установке pyannote-audio

```bash
# Установите по одной
pip install torch torchaudio
pip install transformers
pip install pyannote-audio
```

### 3. Ошибка "Microsoft Visual C++ required" (Windows)

- Скачайте и установите: https://aka.ms/vs/17/release/vc_redist.x64.exe

### 4. Медленная установка

```bash
# Используйте зеркало PyPI (для России)
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Установка с GPU поддержкой

### NVIDIA GPU (CUDA)

```bash
# Установите PyTorch с CUDA
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Остальные зависимости
pip install -r requirements.txt
```

### AMD GPU (ROCm) - только Linux

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
pip install -r requirements.txt
```

### Apple Silicon (M1/M2/M3) - macOS

```bash
# PyTorch автоматически использует Metal
pip install -r requirements.txt
```

## Минимальные требования

- Python 3.11 или выше
- 8 GB RAM
- 10 GB свободного места
- Интернет для загрузки моделей (только при первом запуске)

## Рекомендуемые требования

- Python 3.11+
- 16 GB RAM
- NVIDIA GPU с 8+ GB VRAM
- 20 GB свободного места
- SSD

## Дополнительная информация

- [Быстрый старт](QUICKSTART_RU.md)
- [Полная документация](README_RU.md)
- [Пример конфигурации](.env.example)
