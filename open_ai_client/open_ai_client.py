import requests
import json

class OpenAIClient:
    def __init__(self, api_key: str, temperature: float = 0.7):
        self.api_key = api_key
        self.temperature = temperature

    def generate_chat_completion(self, prompt: str) -> str:

        endpoint = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "gpt-3.5-turbo",
            "temperature": self.temperature
        }
        
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            print(response)
            print(response.json())
            return "Error occurred while generating chat completion."

