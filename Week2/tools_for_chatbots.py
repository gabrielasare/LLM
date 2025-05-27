# imports

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr


# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4o-mini"
openai = OpenAI()


system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."


# TOOLS
ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
place_availability = {"london": "July 30th, 2025", "paris": "May 29th, 2025", "tokyo": "June 3rd, 2025", "berlin": "June 15th, 2025"}

# for getting the price associated with the provided destination city
def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")

# getting ticket availability
def get_destination_availability(destination_city):
    print(f"Tool get_destination_availability called for {destination_city}")
    city = destination_city.lower()
    return place_availability.get(city, "unknown")
    

# The dictionary structure we are using for our function
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

availability_function = {
    "name": "get_destination_availability",
    "description": "Get the availability of a ticket to the destination city. Call this whenever you need to know the availability of a ticket, for example when a customer asks 'when is the availability for the ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

#include this to the list of tools
tools = [
    {"type": "function", "function": price_function}, 
    {"type": "function", "function": availability_function}
]


# this functions handles chats, including history, between the AI API and user
# this functions allows the LLM to use at tool for determining prices for commuting to cities
def chat(message, history):
    messages = [{'role': 'system', 'content':system_message}] + history + [{'role': 'user', 'content': message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    
    if response.choices[0].finish_reason=='tool_calls':
        message = response.choices[0].message
        response = handle_tool_call(message) # handle to tool response
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)
    
    return response.choices[0].message.content


# for handling tool responses and taking the appropriate action

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    function_name = tool_call.function.name
    
    # for getting ticket sales
    if function_name == 'get_ticket_price':
        city = arguments.get('destination_city')
        price = get_ticket_price(city)
        response = {
            "role": "tool",  
            "content": json.dumps({"destination_city": city, "price": price}),
            "tool_call_id": tool_call.id
        }
    # for handling the ticket availability
    elif function_name == 'get_destination_availability':
        city = arguments.get('destination_city')
        availability = get_destination_availability(city)
        response = {
            "role": "tool",  
            "content": json.dumps({"destination_city": city, "availablity": availability}),
            "tool_call_id": tool_call.id
        }
        
    return response


gr.ChatInterface(fn=chat, type="message").launch()




