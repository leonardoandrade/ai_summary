import requests
import json

class OpenAIClient:
    def __init__(self, api_key: str, temperature: float = 0.7):
        """
        Initialize the OpenAI API client with the provided API key and temperature.
        
        Args:
            api_key (str): Your OpenAI API key.
            temperature (float): The temperature parameter affects the randomness of the output.
                                 It ranges from 0 to 1 (default is 0.7).
        """
        self.api_key = api_key
        self.temperature = temperature

    def generate_chat_completion(self, prompt: str) -> str:
        """
        Generate a chat completion using OpenAI's ChatGPT API.
        
        Args:
            prompt (str): The user's message prompt to generate a response from ChatGPT.
        
        Returns:
            str: The generated chat completion response from ChatGPT.
        """
        endpoint = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature
        }
        
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return "Error occurred while generating chat completion."

