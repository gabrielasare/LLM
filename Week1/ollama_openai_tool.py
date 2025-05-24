'''
To demonstrate your familiarity with OpenAI API, and also Ollama, build a tool that takes a 
technical question, and responds with an explanation.
'''

# imports
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
import json


# constants
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
OLLAMA_API = "http://localhost:11434/api/chat"

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")

MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'
HEADERS = {"Content-Type": "application/json"}


# set up environment
openai=OpenAI()


# Get gpt-4o-mini to answer, with streaming
def openai_response(messages):
    stream = openai.chat.completions.create(
        model=MODEL_GPT,
        messages=messages,
        stream=True
    )
    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```","").replace("markdown", "")
        update_display(Markdown(response), display_id=display_handle.display_id)

def llama_response(payload):
    response = requests.post(OLLAMA_API, json=payload, headers=HEADERS, stream=True)

    response_text = ""
    display_handle = display(Markdown(""), display_id=True)

    for line in response.iter_lines():
        if line:
            try: #Decode each line and parse it as a JSON object.
                data = line.decode("utf-8")
                json_data = json.loads(data)
                content = json_data.get("message", {}).get("content", "")
                response_text += content
                response_text = response_text.replace("```", "").replace("markdown", "")
                update_display(Markdown(response_text), display_id=display_handle.display_id)
            except json.JSONDecodeError as e:
                print("JSON decoding error:", e)


def main():
    system_prompt = f"You are excellent at answering questions of all kinds, ranging from technical \
    to philosophical questions. You are excellent at understanding questions and providing True and \
    excellent responses to the questions"

    question = input("Enter your question")
    messages = [
        {'role': 'system', 'content': system_prompt},
        {"role": "user", "content": question}
    ]
    
    payload = {
            "model": MODEL_LLAMA,
            "messages": messages,
            "stream": True
        }

    print("\nChatGPT Response\n================================\n")
    openai_response(messages)

    print("\nOLLama Response\n================================\n")
    llama_response(payload)
    
    
if __name__=="__main__":
    main()
    
