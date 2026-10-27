import os
from dotenv import load_dotenv
import chromadb
load_dotenv()
from pypdf import PdfReader
from mistralai.client import Mistral
#pdf reader
reader=PdfReader("mypdf.pdf")
text=""
for page in reader.pages:
    text+=page.extract_text()

    #chunking
    def chunks_text(text,chunk_size=50,overlap=20):
        start=0
        chunks=[]
        while start<len(text):
            chunks.append(text[start:start+chunk_size])
            start+=chunk_size-overlap
        return chunks
chunks=chunks_text(text)
# embedding and store in db

client = chromadb.Client()
collection = client.create_collection("chatwithpdf")

# for i in range(len(chunks)):
#     print(str(i))

collection.add(
    documents = chunks,
    ids=[str(i) for i in range(len(chunks))],
)

# user input 

user_input = input("Ask question to pdf :")

relevant = collection.query(
    query_texts=user_input,
    n_results = 4
)
print(relevant)
print(relevant.documents)
# injection + generation

user_prompt = """
give answer using following context only:
{relevant}
your answer must be in this pdf only if not found in context then say "answer not found in pdf"

here is question : {user_input}
"""

client = Mistral(api_key = os.getenv("MISTRAL_API_KEY"))

response = client.chat.complete(
    model="mistral-small-latest",
    temperature=0.6,
    messages=[
        {
            "role":"user",
            "content":user_prompt,
        },
    ]
)

# print(response.choices[0].message.content)

