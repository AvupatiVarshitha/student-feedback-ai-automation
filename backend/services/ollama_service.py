import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:latest"


def analyze_feedback(prompt):

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    response.raise_for_status()

    return response.json()["response"]