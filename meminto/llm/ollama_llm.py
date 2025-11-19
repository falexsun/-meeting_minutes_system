import requests
import time
from typing import Optional


class OllamaLLM:
    """
    Класс для работы с локальной LLM через Ollama.
    Ollama использует OpenAI-совместимый API на http://localhost:11434
    """

    def __init__(
        self,
        model: str,
        url: str = "http://localhost:11434/api/generate",
        temperature: float = 0.5,
        max_tokens: int = 4000,
    ):
        self.model = model
        self.url = url
        self.temperature = temperature
        self.max_tokens = max_tokens

    def infer(self, system_prompt: str, user_prompt: str) -> str:
        """
        Отправляет запрос к Ollama и получает ответ.

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
        print(f"Размер промпта: {len(parameters['prompt'])} символов")
        print(f"Параметры: temperature={parameters['options']['temperature']}, num_predict={parameters['options']['num_predict']}")

        # Retry логика для случаев, когда Ollama перезагружается (502 Bad Gateway)
        max_retries = 3
        retry_delay = 5  # секунды

        for attempt in range(max_retries):
            try:
                # Увеличиваем таймаут до 300 секунд (5 минут) для генерации
                response = requests.post(url=self.url, headers=headers, json=parameters, timeout=300)
                response.raise_for_status()

                response_data = response.json()

                # Для Ollama API /api/generate формат: {"response": "текст"}
                if "response" in response_data:
                    return response_data["response"]
                else:
                    raise ValueError(f"Неожиданный формат ответа от Ollama: {response_data}")

            except requests.exceptions.HTTPError as e:
                # Если 502 Bad Gateway - повторяем попытку
                if e.response is not None and e.response.status_code == 502:
                    if attempt < max_retries - 1:
                        print(f"Получена ошибка 502 (Ollama перезагружается). Попытка {attempt + 1}/{max_retries}. Ожидание {retry_delay} сек...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"Ошибка 502 после {max_retries} попыток")
                
                # Для других ошибок или если исчерпаны попытки - выводим информацию
                print(f"Ошибка при обращении к Ollama: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Код ответа: {e.response.status_code}")
                    print(f"Текст ответа: {e.response.text[:500]}")
                raise
            
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при обращении к Ollama: {e}")
                raise
        
        # Если дошли сюда - все попытки провалились
        raise RuntimeError(f"Не удалось получить ответ от Ollama после {max_retries} попыток")

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
        Создает параметры для запроса к Ollama API /api/generate.
        
        Формат для /api/generate:
        {
          "model": "model_name",
          "prompt": "combined_prompt",
          "stream": false,
          "options": {...}
        }
        """
        # Объединяем system_prompt и user_prompt в один промпт
        combined_prompt = f"{system_prompt}\n\n{user_prompt}"

        parameters = {
            "model": self.model,
            "prompt": combined_prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            }
        }

        return parameters
