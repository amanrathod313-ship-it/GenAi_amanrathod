import os
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()
mistral = Mistral(api_key=os.getenv("MISTRAL_KEY"))
response = mistral.chat.complete(
    model="mistral-small-latest",
    messages=[
        {"role": "system", "content": "Welcome to **St. Jude Care Hospital**, a trusted multi-specialty healthcare facility dedicated to delivering high-quality, compassionate medical care to our community. "
        "Our hospital is equipped with modern medical technology and staffed by an experienced team of doctors, nurses, and specialists who work together to ensure complete patient care. We offer 24/7 emergency services,"
        " advanced surgical treatments, thorough diagnostic testing, routine health checkups, and comfortable inpatient care."
        " By combining advanced medical practices with a personalized, patient-first approach, St. Jude Care Hospital strives to create a safe, warm, and healing environment for every patient who walks through our doors.."},

        {"role": "user", "content": "What are the services provided by St. Jude Care Hospital?"}
    ]
)
print(response.choices[0].message.content)
