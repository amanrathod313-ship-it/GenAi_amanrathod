
import os
import json
from mistralai.client import Mistral
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()

# Initialize Mistral client
ai_client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

# Cafe items and their prices
cafe_items = {
    "pepsi": 29,
    "coke": 29,
    "water": 19,
    "coffee": 49,
    "tea": 29,
    "icecream": 99,
    "cake": 199,
    "spring roll": 49,
    "samosa": 29,
    "pasta": 149,
    "puff": 30
}


# Function to display the complete menu
def display_menu():
    menu_list = []

    for name, amount in cafe_items.items():
        menu_list.append(f"{name} - {amount}")

    return json.dumps(menu_list)


# Function to retrieve information from the internet
def search_online(search_query):
    with DDGS() as search_engine:
        search_results = list(
            search_engine.text(search_query, max_results=3)
        )

    if search_results:
        output = ""

        for entry in search_results:
            output += entry["body"] + "\n"

        return output

    return f"{search_query} not found"


# Function to find the cost of a cafe item
def find_price(item_name):
    item_name = item_name.lower().strip()

    if item_name in cafe_items:
        return f"{item_name} cost {cafe_items[item_name]}"

    return "Item not found"


# Available tools for the AI model
available_tools = [
    {
        "type": "function",
        "function": {
            "name": "display_menu",
            "description": "Get the complete cafe menu with item names and prices",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_online",
            "description": "Search the internet for information related to the user's query",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {
                        "type": "string",
                        "description": "The topic to search on the internet"
                    }
                },
                "required": ["search_query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_price",
            "description": "Retrieve the price of a specific cafe menu item",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "Name of the cafe item"
                    }
                },
                "required": ["item_name"]
            }
        }
    }
]


# Function to execute the selected tool
def execute_tool(tool_name, parameters):

    if tool_name == "display_menu":
        return display_menu()

    elif tool_name == "search_online":
        return search_online(parameters["search_query"])

    elif tool_name == "find_price":
        return find_price(parameters["item_name"])

    return "Tool not found"


# Get the user's question
user_question = input("BOT : ")

conversation = [
    {
        "role": "system",
        "content": (
            "You are a friendly cafe helpdesk bot. "
            "Use the available tools to answer questions about menu items and prices. "
            "For questions unrelated to the cafe, use search_online. "
            "Provide short and clear responses."
        )
    },
    {
        "role": "user",
        "content": user_question
    }
]


# Send the request to Mistral
api_response = ai_client.chat.complete(
    model="mistral-small-latest",
    temperature=0.2,
    messages=conversation,
    tools=available_tools,
    tool_choice="auto"
)

assistant_reply = api_response.choices[0].message


# Process tool requests
if assistant_reply.tool_calls:

    conversation.append(assistant_reply)

    for requested_tool in assistant_reply.tool_calls:

        function_name = requested_tool.function.name

        print(f"Tool Used : {function_name}")
        print(f"Arguments Used : {requested_tool.function.arguments}")

        function_args = json.loads(
            requested_tool.function.arguments
        )

        tool_result = execute_tool(
            function_name,
            function_args
        )

        print("Tool Execution Result :")
        print(f"{function_name} => {tool_result}")

        conversation.append({
            "role": "tool",
            "name": function_name,
            "content": str(tool_result),
            "tool_call_id": requested_tool.id
        })


    # Generate the final answer
    final_response = ai_client.chat.complete(
        model="mistral-small-latest",
        temperature=0.2,
        messages=conversation
    )

    print(final_response.choices[0].message.content)

else:

    print(assistant_reply.content)
