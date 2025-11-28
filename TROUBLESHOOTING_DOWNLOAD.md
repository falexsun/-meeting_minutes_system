# Решение проблем с загрузкой моделей pyannote

## Проблема 1: Загрузка зависает на 0%

Если при запуске программы шкала загрузки не двигается:
```
pytorch_model.bin:   0%|                                                 | 0.00/5.91M [00:00<?, ?B/s]
```

### ГЛАВНОЕ РЕШЕНИЕ: Отключить Xet Storage

Xet Storage очень медленный на некоторых соединениях. Отключите его:

```powershell
# Установить переменную окружения для отключения Xet
$env:HF_HUB_ENABLE_HF_TRANSFER = "0"

# Запустить программу
python -m meminto.main -f examples/Scoreboard.wav -l russian
```

Или добавьте в `.env` файл:
```env
HF_HUB_ENABLE_HF_TRANSFER=0
```

## Проблема 2: Timeout при загрузке моделей

Если возникает ошибка:
```
ReadTimeoutError: HTTPSConnectionPool(host='cas-bridge.xethub.hf.co', port=443): Read timed out.
```

## Решения (в порядке приоритета)

### Решение 1: Установить hf_xet для ускорения загрузки

```powershell
# Активировать виртуальное окружение
.\venv\Scripts\Activate.ps1

# Установить пакет для более быстрой загрузки
pip install hf_xet

# Запустить программу снова
python -m meminto.main -f examples/Scoreboard.wav -l russian
```

### Решение 2: Увеличить таймаут загрузки

Если hf_xet не помогает, увеличьте таймаут:

```powershell
# Установить переменную окружения для увеличения таймаута
$env:HF_HUB_DOWNLOAD_TIMEOUT = "600"

# Запустить программу
python -m meminto.main -f examples/Scoreboard.wav -l russian
```

### Решение 3: Скачать модели вручную

Если автоматическая загрузка не работает, скачайте модели вручную:

#### Шаг 1: Создайте директорию для моделей

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cache\huggingface\hub"
```

#### Шаг 2: Скачайте модели через huggingface-cli

```powershell
# Установить huggingface-cli если еще не установлен
pip install huggingface_hub[cli]

# Войти в аккаунт Hugging Face
huggingface-cli login

# Скачать модель диаризации
huggingface-cli download pyannote/speaker-diarization-3.1 --local-dir-use-symlinks False

# Скачать модель сегментации
huggingface-cli download pyannote/segmentation-3.0 --local-dir-use-symlinks False

# Скачать модель эмбеддингов
huggingface-cli download pyannote/wespeaker-voxceleb-resnet34-LM --local-dir-use-symlinks False
```

#### Шаг 3: Запустить программу

После успешной загрузки всех моделей:

```powershell
python -m meminto.main -f examples/Scoreboard.wav -l russian
```

### Решение 4: Использовать VPN или прокси

Если проблема в блокировке доступа к Hugging Face:

```powershell
# Настроить прокси (замените на ваш прокси)
$env:HTTP_PROXY = "http://your-proxy:port"
$env:HTTPS_PROXY = "http://your-proxy:port"

# Запустить программу
python -m meminto.main -f examples/Scoreboard.wav -l russian
```

### Решение 5: Скачать модели на другом компьютере

Если сервер имеет ограничения сети:

1. **На компьютере с интернетом:**
   ```powershell
   # Скачать модели
   python -c "from pyannote.audio import Pipeline; Pipeline.from_pretrained('pyannote/speaker-diarization-3.1', use_auth_token='YOUR_TOKEN')"
   ```

2. **Найти директорию с моделями:**
   ```powershell
   # Windows
   dir "$env:USERPROFILE\.cache\huggingface\hub"
   
   # Linux
   ls ~/.cache/huggingface/hub
   ```

3. **Скопировать папку на сервер:**
   - Архивировать: `~/.cache/huggingface/hub`
   - Перенести на сервер
   - Распаковать в ту же директорию

4. **На сервере проверить:**
   ```powershell
   ls "$env:USERPROFILE\.cache\huggingface\hub"
   ```

### Решение 6: Использовать другое зеркало Hugging Face

Если основной сервер недоступен:

```powershell
# Установить переменную для зеркала (например, HF Mirror в Китае)
$env:HF_ENDPOINT = "https://hf-mirror.com"

# Запустить программу
python -m meminto.main -f examples/Scoreboard.wav -l russian
```

## Проверка успешной загрузки

После выполнения любого из решений, проверьте наличие моделей:

```powershell
# Проверить кэш Hugging Face
ls "$env:USERPROFILE\.cache\huggingface\hub"

# Должны быть папки вида:
# models--pyannote--speaker-diarization-3.1
# models--pyannote--segmentation-3.0
# models--pyannote--wespeaker-voxceleb-resnet34-LM
```

## Дополнительные рекомендации

### Включить Developer Mode в Windows (для symlinks)

Если видите предупреждение о symlinks:

1. Откройте **Параметры Windows** → **Обновление и безопасность** → **Для разработчиков**
2. Включите **Режим разработчика**
3. Перезапустите PowerShell

### Освободить место на диске

Модели занимают примерно:
- `speaker-diarization-3.1`: ~15 MB
- `segmentation-3.0`: ~6 MB
- `wespeaker-voxceleb-resnet34-LM`: ~80 MB

**Итого:** ~100 MB свободного места

### Проверка соединения с Hugging Face

```powershell
# Проверить доступность Hugging Face
Test-NetConnection huggingface.co -Port 443

# Проверить доступность XetHub
Test-NetConnection cas-bridge.xethub.hf.co -Port 443
```

## Если ничего не помогло

Откройте issue на GitHub с полным выводом ошибки:
https://github.com/falexsun/-meeting_minutes_system/issues

Или свяжитесь со службой поддержки Hugging Face:
https://huggingface.co/support
