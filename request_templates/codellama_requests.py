# In this file we define functions that allows us to send requests and queries to codellama-instruct in the specified format
# Requests are made to the API endpoint provided by Ollama

import requests
import json

def query_code_llama(prompt, system_instruction="You are a helpful coding assistant."):
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

# Example usage
if __name__ == "__main__":
    # Example 1: Basic usage
    result = query_code_llama("Write a Python function to compute the factorial of a number.")
    print("Response:", result)

    # Example 2: With custom system instruction
    custom_result = query_code_llama(
        prompt="Write a Python function to sort a list.",
        system_instruction="You are an expert Python programmer. Provide concise and efficient solutions."
    )
    print("\nCustom Response:", custom_result)
