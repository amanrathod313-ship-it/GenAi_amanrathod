import os
from dotenv import load_dotenv
from mistralai.client import Mistral
load_dotenv()
client=Mistral(api_key=os.getenv("MISTRAL_KEY"))
name=input("Enter your full name: ")
age=input("Enter  age: ")
gender=input("Enter  gender: ")
mobile=input("Enter  mobile number: ")
disease=input("Enter  disease: ")
response=client.chat.complete(
model="mistral-small-latest",
messages=[
        {
            "role": "system",
            "content": """You are a helpful assistant that summarizes patient information."
             "You are a medical information summarization assistant. "
            "Summarize patient information clearly and professionally. "
            "provide treatment advice."""    
        },
        {
            "role": "user",
            "content": 
            f"Patient Information:\n"
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"Gender: {gender}\n"
            f"Mobile Number: {mobile}\n"
            f"Disease: {disease}\n"
            },
        
    ]

)
print(response.choices[0].message.content)