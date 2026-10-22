import os
import json
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()
client=Mistral(api_key=os.getenv("MISTRAL_KEY"))
car=input("Enter car:")
response=client.chat.complete(
    model="mistral-small-latest",
    temperature=0.2,
    response_format={"type":"json_object"},
    max_tokens=100,
    messages=[
        { 
            "role":"system",
            "content":"""you are professional car analyst"
            "format":"structure all outputs in json format"""
        },
        {
            "role":"user",
            "content":f"{car}"
        },
    ]
)

#print(response.choices[0].message.content)
raw=response.choices[0].message.content
print(raw)
try:
    data=json.loads(raw)
    print(data)
except json.JSONDecodeError:
    print("error while prase to json..")