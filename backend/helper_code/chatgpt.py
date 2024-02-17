import os
import requests
from dotenv import load_dotenv

api_key = os.getenv("OPEN_AI_KEY")

def ask_gpt(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4-0125-preview",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4096
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None