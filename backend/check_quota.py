import requests
from config import config

response = requests.post(
    f"{config.GEMINI_URL}?key={config.GEMINI_API_KEY}",
    json={"contents": [{"parts": [{"text": "hello"}]}]},
)
print(response.status_code)
print(response.text)