import os
import json 
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENAI_APIKEY")

def call(text:str):
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
          "content": f"Your are an agent that pro resume for students using this text : {text}"
        }
      ],
    "reasoning": {"enabled": True}
  })

    )
    response = response.json()
    response = response['choices'][0]['message']
    print(response)
    return response
