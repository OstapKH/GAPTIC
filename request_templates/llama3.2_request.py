import requests
import json

def query_llama_3_2(prompt, system_instruction=None, tools=None):
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
        "temperature": 1.5
    }


    response = requests.post(LLAMA_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result.get("response", "No response received.")
    else:
        return f"Error: {response.status_code} - {response.text}"

def extract_paraphrased_sentence(response):
    """
    Extracts the paraphrased sentence from the response.
    Assumes the response is in the format: "New sentence: {new_sentence}"
    """
    if "New sentence:" in response:
        return response.split("New sentence:")[1].strip()
    return "No paraphrased sentence found."

def return_prompt_with_sentence(sentence):
    prompt = f"Your task is to paraphrase the sentence while keeping the same semantic. I will give you a sentence in such format: [old_sentence]. You must return new sentence in such format: \"New sentence: [new_sentence]\". Here is the old sentence: [{sentence}]"
    return prompt



if __name__ == "__main__":
    # Example: With custom system instruction    sentence_to_paraphrase = "Do not use execute(), which includes cursor.execute() for any SQL queries."
    my_prompt = return_prompt_with_sentence("Do not use execute(), which includes cursor.execute() for any SQL queries.")
    custom_result = query_llama_3_2(
        prompt=my_prompt,
    )

    print("\nCustom Response:", custom_result)
    paraphrased_sentence = extract_paraphrased_sentence(custom_result)
    print("\nParaphrased Sentence:", paraphrased_sentence)