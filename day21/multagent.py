
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)


# Common AI Agent Function
def run_agent(role, content):

    response = client.chat.complete(
        model="mistral-small-latest",
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": role
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )

    return response.choices[0].message.content


# Customer Input
customer = input("\nEnter Customer Complaint: ")


# AGENT 1 - Complaint Analyzer
print("\nAgent 1: Complaint Analysis Started...")

analysis = run_agent(
    "You are a Professional Customer Complaint Analyzer. "
    "Understand the customer's problem, identify the main issue "
    "and explain what help the customer needs. "
    "Do not invent missing information.",

    customer
)

print("Agent 1: Analysis Completed.")


# AGENT 2 - Support Classifier
print("\nAgent 2: Classification Started...")

classification = run_agent(
    "You are a Customer Support Classification Agent. "
    "Analyze the complaint and identify: "
    "1. Category: Delivery, Payment, Product, Technical or General. "
    "2. Priority: Low, Medium or High. "
    "3. Sentiment: Positive, Neutral or Negative. "
    "Explain the classification briefly.",

    f"Customer Complaint: {customer}\n"
    f"Analysis: {analysis}"
)

print("Agent 2: Classification Completed.")


# AGENT 3 - Reply Generator
print("\nAgent 3: Reply Generation Started...")

final_reply = run_agent(
    "You are a Professional Customer Support Executive. "
    "Generate a polite, friendly and professional reply. "
    "Acknowledge the customer's issue and suggest useful next steps. "
    "Never promise refunds, replacements or delivery dates "
    "unless confirmed in the provided information.",

    f"Customer Complaint: {customer}\n"
    f"Analysis: {analysis}\n"
    f"Classification: {classification}"
)

print("Agent 3: Reply Generation Completed.")


# FINAL OUTPUT
print("\n========== CUSTOMER SUPPORT REPORT ==========")

print("\nCUSTOMER COMPLAINT:")
print(customer)

print("\nCOMPLAINT ANALYSIS:")
print(analysis)

print("\nCATEGORY AND PRIORITY:")
print(classification)

print("\nGENERATED CUSTOMER REPLY:")
print(final_reply)

print("\n========== TASK COMPLETED ==========")
