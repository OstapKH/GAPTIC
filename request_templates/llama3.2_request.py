import requests
import json

def query_llama_3_2(prompt, system_instruction=None, tools=None):
    # Define the API endpoint for LLaMA 3.2
    LLAMA_URL = "http://localhost:11434/api/generate"  # Update with the actual endpoint

    # Construct the system header
    system_header = "<|start_header_id|>system<|end_header_id|>\n\nCutting Knowledge Date: December 2023\n\n"
    if system_instruction:
        system_header += f"{system_instruction}\n\n"
    if tools:
        system_header += "When you receive a tool call response, use the output to format an answer to the original user question.\n\nYou are a helpful assistant with tool calling capabilities.\n\n"
    system_header += "<|eot_id|>\n"

    # Construct the user message
    user_message = f"<|start_header_id|>user<|end_header_id|>\n\n{prompt}\n<|eot_id|>\n"

    # Combine headers and messages
    formatted_prompt = system_header + user_message

    # Define the payload
    payload = {
        "model": "llama:3.2",  # Update with the correct model identifier if needed
        "prompt": formatted_prompt,
        "stream": False,
        "options": {
            "num_predict": 200  # Adjust as needed
        }
    }

    # Send the request
    response = requests.post(LLAMA_URL, json=payload)

    # Parse the response
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "No response received.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Example usage
if __name__ == "__main__":
    # Example 1: Basic usage
    result = query_llama_3_2("Write a Python function to compute the factorial of a number.")
    print("Response:", result)

    # Example 2: With custom system instruction and tools
    custom_result = query_llama_3_2(
        prompt="Write a Python function to sort a list.",
        system_instruction="You are an expert Python programmer. Provide concise and efficient solutions.",
    )
    print("\nCustom Response:", custom_result)