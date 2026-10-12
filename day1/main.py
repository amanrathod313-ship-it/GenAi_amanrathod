import os
from pathlib import Path
from mistralai.client import Mistral
from dotenv import load_dotenv

# Load .env from the script's directory as well as the current working directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY") or os.getenv("MASTER_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found. Please set it in your .env file.")

client = Mistral(api_key=api_key)

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[
        {"role": "user", "content": "What is ai?"}
    ],
)

print(response.choices[0].message.content)