import json
import urllib.request


# NVIDIA API configuration
API_KEY = "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"
URL = "https://integrate.api.nvidia.com/v1/chat/completions"

MODEL = "meta/llama-3.1-8b-instruct"


# Common function used by every agent
def ask_ai(role, question):

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": role
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    request = urllib.request.Request(
        URL,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "AgenticAIWorkshop"
        },
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(
            response.read().decode("utf-8")
        )

    return result["choices"][0]["message"]["content"]