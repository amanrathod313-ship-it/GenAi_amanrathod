import os
import json
from mistralai.client import Mistral
from dotenv import  load_dotenv

load_dotenv()

client=Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
menu={
    "piza":120,
    "burger":100,
    "sandwich":80,
    "fries":50,
    "soda":30,                  
    "water":20,
    "applle juice":40,
}
def get_menu():
    res=[]
    for item in menu:
        res.append(f"{item}:{menu[item]}")
    return res
tools=[
    {
        "type":"function",
        "function":{
            "name":"get_menu",
            "description":"show menu with price",
            "parameters":{
                "type":"object",
                "properties":{}
            }
        }
    }
]
user_input=input("bot : ")
message=[{
    "role":"user",
    "content":user_input
}]
msg=client.chat.complete(
    model="mistral-small-latest",
    messages=message,
    tools=tools,
)
response=msg.choices[0].message

if response.tool_calls:
    message.append(response)
    for tc in response.tool_calls:
        if tc.function.name=="get_menu":
           result=get_menu()
        formatted_result=json.dumps(result)
        message.append(
            {
                "role":"tool",
                "content":formatted_result,
                "tool_call_id":tc.id
            }
        )
        final=client.chat.complete(
            model="mistral-small-latest",
            temperature=0.1,
            messages=message
        )
        print(final.choices[0].message.content)
    else:
        print(response.content)
    
