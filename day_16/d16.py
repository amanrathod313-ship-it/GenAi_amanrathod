import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection =client.get_or_create_collection("prilytixs")
collection.add(
documents=["Generative AI (GenAI) is a type of Artificial Intelligence (AI) that can create new content such as text, images, videos, audio, and computer code.","Java is a popular, high-level, object-oriented programming language developed by Sun Microsystems. It is widely used for web development, mobile applications, desktop software, and enterprise systems."],
metadatas=[{"sources":"gpt"},{"sources":"a.pdf"}],
ids=["docs1","docs2"]
)
result=collection.query(
    query_texts=["what Gen Ai ?"],
    n_results=1

)
print(result)