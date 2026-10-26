import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# User inputs
topic = input("Enter blog topic: ")
style = input("Enter writing style (Professional / Friendly / Informative): ")
word_count = input("Enter approximate word count: ")

# Generate blog
response = client.chat.stream(
    model="mistral-small-latest",
    temperature=0.7,
    messages=[
        {
            "role": "system",
            "content": """
            You are a professional AI blog writer.
            Write engaging, clear, and original blog posts.
            Use a suitable title, introduction, headings,
            conclusion, and relevant examples.
            Stay focused on the user's topic.
            """
        },
        {
            "role": "user",
            "content": f"""
            Write a blog post with the following details:

            Topic: {topic}
            Writing style: {style}
            Approximate word count: {word_count}

            Include:
            1. An attractive title
            2. An engaging introduction
            3. At least three useful sections with headings
            4. Relevant examples
            5. A conclusion
            """
        },
    ],
)

print("\n" + "=" * 50)
print("YOUR AI-GENERATED BLOG")
print("=" * 50 + "\n")

for chunks in response:
    content = chunks.data.choices[0].delta.content
    if content:
        print(content, end="", flush=True)

print("\n\nBlog generation completed!")