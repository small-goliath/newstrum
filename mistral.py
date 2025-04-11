import requests
from logger import get_logger

log = get_logger('GPT')

class Mistral:
    def __init__(self, api_key: str, uri: str):
        self.uri = uri
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze(self, prompt: str, model: str) -> str:
        log.info("🔍 분석 중...")
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "top_p": 1,
            "stream": False,
            "safe_prompt": False
        }

        response = requests.post(self.uri, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()
        log.info(f"🎯 analyze succeed!: {data['usage']['completion_tokens']} completion tokens usage.")

        return data["choices"][0]["message"]["content"]