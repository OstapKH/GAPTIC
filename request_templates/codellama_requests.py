# In this file we define functions that allows us to send requests and queries to codellama-instruct in the specified format
# Requests are made to the API endpoint provided by Ollama

import requests
import json

def query_code_llama(prompt, system_instruction="You should only output functioning, bug-free and secure code according to the instructions. Do not output any text that is not interpretable by python. Do not include any comments in your code. Your output will be run directly in a python interpreter, so treat it as such. Return code in [PYTHON] tags and [/PYTHON] tags."):
    # Ollama server URL
    OLLAMA_URL = "http://localhost:11434/api/generate"

    # Format the input as per Ollama's expected template
    formatted_prompt = f"[INST] <<SYS>>{system_instruction}<</SYS>>\n\n{prompt} [/INST]"

    # Define the payload
    payload = {
        "model": "codellama:7b-instruct",
        "prompt": formatted_prompt,
        "stream": False,
        "options": {
            "num_predict": 200  # Limit output to approximately 200 words
        }
    }

    # Send the request
    response = requests.post(OLLAMA_URL, json=payload)

    # Parse the response
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "No response received.")
    else:
        return f"Error: {response.status_code} - {response.text}"
