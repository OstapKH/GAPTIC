import requests
import json

def query_deepseek(system_instruction, user_message, model="deepseek-r1:1.5b"):
    url = "http://localhost:11434/api/chat"  # Default Ollama API endpoint
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_message}
        ],
        "stream": False  # Set to True if you want streaming responses
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        # Extract the content from the nested message structure
        return response_data.get("message", {}).get("content", "No response from model")
    else:
        return f"Error: {response.status_code}, {response.text}"

