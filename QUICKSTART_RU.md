# Быстрый старт - Протоколирование совещаний

## Что было сделано

Проект Meminto адаптирован для:
- ✅ Полной поддержки русского языка
- ✅ Локальной обработки через Ollama (без передачи данных в облако)
- ✅ Работы с совещаниями длительностью 1-2 часа

## Установка за 5 минут

### 1. Установите зависимости автоматически

**Windows (самый простой способ):**
```powershell
# Дважды кликните на install.bat
# ИЛИ в PowerShell/CMD:
.\install.bat
```

**Linux / macOS:**
```bash
# Запустите скрипт установки
./install.sh
```

**Или вручную через pip:**
```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте (Windows)
.\venv\Scripts\activate

# Активируйте (Linux/macOS)
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Установите Ollama

**Windows:**
```bash
# Скачайте с https://ollama.com/download и установите
# После установки откройте командную строку:
ollama pull qwen2.5:7b
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b
```

### 3. Настройте .env файл

```bash
# Скопируйте пример
cp .env.example .env

# Отредактируйте .env и добавьте токен Hugging Face:
# Получить можно тут: https://huggingface.co/settings/tokens
# После регистрации и принятия условий: https://huggingface.co/pyannote/speaker-diarization
```

Минимальная конфигурация `.env`:
```env
HUGGING_FACE_ACCESS_TOKEN=ваш_токен
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_URL=http://localhost:11434/api/chat
OLLAMA_MAX_TOKENS=8000
```

### 4. Запустите обработку

```bash
# Не забудьте активировать виртуальное окружение!
# Windows:
.\venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# Базовое использование
python meminto/main.py -f путь/к/аудио.wav -l russian --use-ollama

# С указанием папки для результатов
python meminto/main.py -f meeting.wav -o output -l russian --use-ollama
```

## Результат

В папке `output` вы получите:
- `diarization.txt` - кто и когда говорил
- `transcript.txt` - полная расшифровка
- `meeting_minutes.txt` - **структурированный протокол**

## Формат протокола

```markdown
**Цели:**
- Список целей совещания

**Решения:**
- Все принятые решения

**Назначенные задачи:**
- SPEAKER_01: Что нужно сделать
- SPEAKER_02: Что нужно сделать

**Дополнительные заметки:**
- Важные моменты обсуждения
```

## Требования к системе

**Минимум:**
- 8 GB RAM
- 10 GB свободного места

**Рекомендуется для совещаний 1-2 часа:**
- 16 GB RAM
- NVIDIA GPU с 8+ GB VRAM
- 20 GB свободного места

## Рекомендации по моделям

| Модель | Размер | Качество РУС | Скорость | GPU RAM |
|--------|--------|--------------|----------|---------|
| qwen2.5:3b | ~2 GB | ⭐⭐⭐ | ⚡⚡⚡ | 4 GB |
| qwen2.5:7b | ~4 GB | ⭐⭐⭐⭐ | ⚡⚡ | 8 GB |
| qwen2.5:14b | ~8 GB | ⭐⭐⭐⭐⭐ | ⚡ | 16 GB |
| llama3.2 | ~4 GB | ⭐⭐⭐ | ⚡⚡⚡ | 8 GB |

**Для начала рекомендуем:** `qwen2.5:7b` - оптимальное соотношение качества и скорости.

## Типичные проблемы

### Ollama не отвечает
```bash
# Проверьте статус
curl http://localhost:11434/api/tags

# Если не работает - перезапустите Ollama
```

### Нехватка памяти GPU
```bash
# Используйте модель меньшего размера
ollama pull qwen2.5:3b

# В .env измените:
OLLAMA_MODEL=qwen2.5:3b
```

### Медленная обработка
1. Убедитесь, что Ollama использует GPU
2. Разбейте аудио на части по 30-40 минут
3. Используйте модель меньшего размера

## Конфиденциальность

**100% локальная обработка:**
- Диаризация: локально (pyannote.audio)
- Транскрипция: локально (Whisper)
- Генерация протокола: локально (Ollama)

**Никакие данные не покидают ваш сервер!**

Интернет нужен только для загрузки моделей при первом запуске.

## Дополнительная информация

- **Подробная установка:** [INSTALL_RU.md](INSTALL_RU.md)
- **Полная документация:** [README_RU.md](README_RU.md)
- **Пример конфигурации:** [.env.example](.env.example)
- **Оригинальный проект:** https://github.com/FlorianSchepers/Meminto
