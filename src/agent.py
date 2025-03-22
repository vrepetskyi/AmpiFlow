
import requests
import json
import sys

url = "https://api.asi1.ai/v1/chat/completions"

if len(sys.argv) < 1:
  print("No required parameter: file with token for AI")
  sys.exit(1)

token_file = sys.argv[1]

with open(token_file, 'r') as file:
  token = file.read().rstrip()

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
  'Authorization': f'Bearer {token}'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)