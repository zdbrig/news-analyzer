import json
import requests
import logging  # Import the logging module
from utils.config import read_config



def read_request_file(request_file_name):
    with open(request_file_name, "r") as file:
        content = file.read()
    return content

def escape_content(content):
    """Escapes the given content using json.dumps and returns it."""
    escaped_content = json.dumps(content)
    logging.debug(f"Escaped content: {escaped_content}")  # Log the escaped content
    return escaped_content


def make_request(content , request):
    """Makes a POST request with the given content and returns the response."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+read_config()["authorization"],
    }
    data = {
        "model": read_config()["openai-model"],
        "messages": [
        {"role": "assistant", "content": read_request_file(request["rules"]) },
        {"role": "user", "content": content}]
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=data
    )
    logging.debug(f"Made request with content: {content}")  # Log the request content
    return response


def extract_content(response):
    """Extracts the content from the response and replaces escaped newlines with actual line breaks."""
    content = response.json()["choices"][0]["message"]["content"]
    content = content.replace("\\n", "\n")
    logging.debug(f"Extracted content: {content}")  # Log the extracted content
    return content
