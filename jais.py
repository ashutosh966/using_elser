
import requests
API_TOKEN = "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"

api_url = "https://api-inference.huggingface.co/models/core42/jais-13b-chat"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
context = "The capital of the United Arab Emirates is Abu Dhabi. It is known for its modern architecture and vibrant culture."
question = "What is the capital of UAE?"
payload = {"inputs": f"Context: {context}\nQuestion: {question}"}

response = requests.post(api_url, headers=headers, json=payload)
print(response.json())
