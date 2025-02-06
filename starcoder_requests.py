import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "starcoder2:3b"

def query_starcoder(prompt, system_instruction="You are a helpful coding assistant."):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "system": system_instruction,
        "stream": False,
        "max_tokens": 1000
    }

    response = requests.post(OLLAMA_API_URL, json=payload)
    
    if response.status_code == 200:
        print(response.json())
        return response.json().get("response", "No response from model.")
    else:
        return f"Error: {response.status_code}, {response.text}"

