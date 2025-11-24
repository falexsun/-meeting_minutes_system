import requests
import time
from typing import Optional


class LMStudioLLM:
    """
    Класс для работы с локальной LLM через LM Studio.
    LM Studio использует OpenAI-совместимый API на http://localhost:1234
    """

    def __init__(
        self,
        model: str,
        url: str = "http://localhost:1234/v1/chat/completions",
        temperature: float = 0.5,
        max_tokens: int = 8000,
    ):
        self.model = model
        self.url = url
        self.temperature = temperature
        self.max_tokens = max_tokens

    def infer(self, system_prompt: str, user_prompt: str) -> str:
        """
        Отправляет запрос к LM Studio и получает ответ.

        Args:
            system_prompt: Системный промпт (контекст для модели)
            user_prompt: Пользовательский запрос

        Returns:
            Ответ модели в виде строки
        """
        headers = self._create_headers()
        parameters = self._create_parameters(system_prompt, user_prompt)

        print(f"Url используемый для LLM запроса: {self.url}")
        print(f"Модель: {self.model}")
        print(f"Размер промпта: {len(system_prompt) + len(user_prompt)} символов")
        print(f"Параметры: temperature={self.temperature}, max_tokens={self.max_tokens}")

        # Retry логика для случаев, когда LM Studio перезагружается
        max_retries = 5
        retry_delay = 10  # секунды

        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"⏳ Попытка {attempt + 1}/{max_retries}...")
                else:
                    print(f"🤖 Отправка запроса в LM Studio (таймаут: 60 мин)...")
                
                # Увеличиваем таймаут до 3600 секунд (60 минут) для генерации
                response = requests.post(url=self.url, headers=headers, json=parameters, timeout=3600)
                response.raise_for_status()

                response_data = response.json()

                # Для LM Studio API формат OpenAI: {"choices": [{"message": {"content": "текст"}}]}
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    print("✅ Ответ получен успешно")
                    return response_data["choices"][0]["message"]["content"]
                else:
                    raise ValueError(f"Неожиданный формат ответа от LM Studio: {response_data}")

            except requests.exceptions.HTTPError as e:
                # Если 502 Bad Gateway - повторяем попытку
                if e.response is not None and e.response.status_code == 502:
                    if attempt < max_retries - 1:
                        print(f"⚠️  Получена ошибка 502 (LM Studio перезагружается). Попытка {attempt + 1}/{max_retries}. Ожидание {retry_delay} сек...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"❌ Ошибка 502 после {max_retries} попыток")
                        print("💡 Убедитесь, что LM Studio запущен и модель загружена")
                
                # Для других ошибок или если исчерпаны попытки - выводим информацию
                print(f"Ошибка при обращении к LM Studio: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Код ответа: {e.response.status_code}")
                    print(f"Текст ответа: {e.response.text[:500]}")
                raise
            
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при обращении к LM Studio: {e}")
                raise
        
        # Если дошли сюда - все попытки провалились
        raise RuntimeError(f"Не удалось получить ответ от LM Studio после {max_retries} попыток")

    def _create_headers(self) -> dict:
        """Создает заголовки для HTTP запроса"""
        headers = {
            "Content-Type": "application/json"
        }
        return headers

    def _create_parameters(
        self, system_prompt: str, user_prompt: str
    ) -> dict:
        """
        Создает параметры для запроса к LM Studio API.
        
        Формат OpenAI-совместимого API:
        {
          "model": "model_name",
          "messages": [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."}
          ],
          "temperature": 0.5,
          "max_tokens": 4000
        }
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        parameters = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        return parameters
