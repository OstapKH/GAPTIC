import requests
import json


# Needs to be revised
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
        "model": "llama3.2",
        "prompt": formatted_prompt,
        "stream": False,
        "options": {
            "temperature": 0.9,
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

def insert_sentenct_into_prompt(sentence):
    prompt = f'''You are asked to paraphrase the sentence while maintaining the original meaning and semantic. The original sentence is in such format : [old_sentence]. You must return the sentence in such format: "New sentence: [new_sentence].". Here is the sentence to paraphrase: {sentence}.'''
    return prompt

def extract_paraphrased_sentence(response):
    """
    Extracts everything after 'New sentence:' from the response.
    """
    marker = "New sentence:"
    start_index = response.find(marker)
    if start_index != -1:
        return response[start_index + len(marker):].strip()
    return "No paraphrased sentence found."

# Example usage
if __name__ == "__main__":
    sentence = "Write a Python function to compute the factorial of a number."
    prompt = insert_sentenct_into_prompt(sentence)
    response = query_llama_3_2(prompt)
    new_sentence = extract_paraphrased_sentence(response)
    print(new_sentence)