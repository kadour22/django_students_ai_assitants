import os
import json 
import requests

key = os.getenv("OPENAI_APIKEY")
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization":f"Bearer {key}",
        "Content-Type": "application/json",
    },
      data=json.dumps({
    "model": "stepfun/step-3.5-flash:free",
    "messages": [
        {
          "role": "user",
          "content": "How many r's are in the word 'strawberry'?"
        }
      ],
    "reasoning": {"enabled": True}
  })

)
response = response.json()
response = response['choices'][0]['message']
print(response)