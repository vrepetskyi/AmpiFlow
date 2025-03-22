
import requests
import json

url = "https://api.asi1.ai/v1/chat/completions"

payload = json.dumps({
  "model": "asi1-mini",
  "messages": [
    {
      "role": "user",
      "content": "Hi, tell me about giraffes"
    }
  ],
  "temperature": 0,
  "stream": True,
  "max_tokens": 0
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer sk_c3f0152a767a41b082f52e60d23d747aab8a1d294f8d4e8695d420216a6906fd'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)