# imports
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Some imports for handling images
import base64
from io import BytesIO
from PIL import Image


# Initialization

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4o-mini"
openai = OpenAI()
OLLAMA_API = "http://localhost:11434/api/chat"
MODEL_LLAMA = 'llama3.2'
HEADERS = {"Content-Type": "application/json"}


system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."


# TOOLS
ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
place_availability = {"london": "July 30th, 2025", "paris": "May 29th, 2025", "tokyo": "June 3rd, 2025", "berlin": "June 15th, 2025"}
languages = {"spanish", "french", "chinese", "portuguese", "korean", "russian"}

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
    {"type": "function", "function": availability_function},
]


# this functions handles chats, including history, between the AI API and user
# this functions allows the LLM to use at tool for determining prices for commuting to cities
def chat(history):
    messages = [{"role": "system", "content": system_message}] + history
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    image = None
    
    if response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        image = artist(city)
        response = openai.chat.completions.create(model=MODEL, messages=messages)
        
    reply = response.choices[0].message.content
    history += [{"role":"assistant", "content":reply}]

    # Comment out or delete the next line if you'd rather skip Audio for now..
    talker(reply)
    
    return history, image


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
    
    return response, city




''' 
    AGENT for IMAGE Generation
    function for generating image using DALL-E-3 model behind GPT-4o
'''
def artist(city):
    image_response = openai.images.generate(
            model="dall-e-3",
            prompt=f"An image representing a vacation in {city}, showing tourist spots and everything unique about {city}, in a vibrant pop-art style",
            size="1024x1024",
            n=1,
            response_format="b64_json",
        )
    image_base64 = image_response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))

image = artist("New York City")
#display(image) # this for displaying images in jupyterLab

'''
AGENT AUDIO

Install homebrew if you don't have it already by running this in a Terminal window and following any instructions:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Then install FFmpeg with 
    -> brew install ffmpeg

Verify your installation with
    -> ffmpeg -version

'''
from pydub import AudioSegment
from pydub.playback import play

def talker(message):
    response = openai.audio.speech.create(
      model="tts-1",
      voice="onyx",    # Also, try replacing onyx with alloy
      input=message
    )
    
    audio_stream = BytesIO(response.content)
    audio = AudioSegment.from_file(audio_stream, format="mp3")
    play(audio)

# for transcribing audio into text
def transcribe_audio(audio_file):
    with open(audio_file, "rb") as f:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

'''
TODO: Try to make a translator agent using OLLAMA for translating languages to other languages

'''
sys_prompt = f"You are an excellent assistant for translating languages to different \
languages. You simply translate the provided message to the provided preferred language. \
for example, the user can simply type the name of language or can they can explicityly \
ask you, 'Can you translate to mandarin'"

def llama_translate(language):
    usr_prompt = f"Can you translate the message to this language: {language}"
    messages = [
        {'role': 'system', 'content': sys_prompt},
        {"role": "user", "content": usr_prompt}
    ]
    
    payload = {
            "model": MODEL_LLAMA,
            "messages": messages,
            "stream": True
        }
    response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
    return response.json()['message']['content']
    

# More involved Gradio code as we're not using the preset Chat interface!
# Passing in inbrowser=True in the last line will cause a Gradio window to pop up immediately.

with gr.Blocks() as ui:
    with gr.Row():
        chatbot = gr.Chatbot(height=500, type="messages")
        image_output = gr.Image(height=500)

    with gr.Row():
        text_input = gr.Textbox(label="Chat with our AI Assistant:")
        audio_input = gr.Audio(sources="microphone", type="filepath", label="Or speak to the assistant")

    with gr.Row():
        # voice_output = gr.Audio(label="Bot Voice Reply", autoplay=True)
        clear = gr.Button("Clear")

    def do_entry(message, audio, history):
        if message:
            history += [{"role":"user", "content":message}]
        if audio:
            history += [{"role":"user", "content":transcribe_audio(audio)}]
        return "", None, history

    text_input.submit(do_entry, inputs=[text_input, audio_input, chatbot], outputs=[text_input, audio_input, chatbot]).then(chat, inputs=chatbot, outputs=[chatbot, image_output]
    )

    audio_input.change(do_entry, inputs=[text_input, audio_input, chatbot], outputs=[text_input, audio_input, chatbot]).then(chat, inputs=chatbot, outputs=[chatbot, image_output]
    )

    clear.click(lambda: None, inputs=None, outputs=chatbot, queue=False)


ui.launch(inbrowser=True)
