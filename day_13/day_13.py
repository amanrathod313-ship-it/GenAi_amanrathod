import chromadb

client = chromadb.Client()

collection = client.create_collection(name="doc_genai")

documents =["Artificial Intelligence: AI enables machines to perform tasks such as reasoning, learning, and problem-solving.",

    "Machine Learning: ML is a branch of AI that allows computers to learn patterns from data and make predictions.",

    "Deep Learning: Deep learning uses neural networks with multiple layers to learn complex patterns from large datasets.",

    "Natural Language Processing: NLP enables computers to understand, process, and generate human language.",

    "Generative AI: Generative AI creates new content such as text, images, music, and computer code.",

    "Computer Vision: Computer vision enables machines to analyze and understand images and videos.",

    "Large Language Models: LLMs are AI models trained on large amounts of text to understand and generate language.",

    "AI Chatbots: AI chatbots interact with users, answer questions, and provide automated customer support."]
    


collection.add(
    ids=["1","2","3","4","5","6","7","8"],
    documents=documents
)

result = collection.query(
    query_texts=["What is  ai ?"],
    n_results=3
)

print(result)