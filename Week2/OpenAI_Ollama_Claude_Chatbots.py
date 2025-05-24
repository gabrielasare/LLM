# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from IPython.display import Markdown, display, update_display


# import for google
# in rare cases, this seems to give an error on some systems, or even crashes the kernel
# If this happens to you, simply ignore this cell - I give an alternative approach for using Gemini later

import google.generativeai

# Load environment variables in a file called .env
# Print the key prefixes to help with any debugging

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:5]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:5]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:5]}")
else:
    print("Google API Key not set")


# Connect to OpenAI, Anthropic, Google
openai = OpenAI()
claude = anthropic.Anthropic()
google.generativeai.configure()

# calling ChatGPT API
def call_gpt(gpt_model, gpt_system, gpt_messages, gemini_messages):
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, claude in zip(gpt_messages, gemini_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": claude})
    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    return completion.choices[0].message.content

# calling gemini
def call_gemini(gpt_messages, gemini_messages, gemini_system):
    messages = []
    for gpt, gemini_msg in zip(gpt_messages, gemini_messages):
        messages.append({"role": "user", "parts": gpt})
        messages.append({"role": "assistant", "parts": gemini_msg})
    messages.append({"role": "user", "parts": gpt_messages[-1]})
    gemini = google.generativeai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=gemini_system
    )
    response = gemini.generate_content(messages)
    return response.text

# calling claude
def call_claude(gpt_messages, claude_messages, claude_model, claude_system):
    messages = []
    for gpt, claude_message in zip(gpt_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": claude_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    message = claude.messages.create(
        model=claude_model,
        system=claude_system,
        messages=messages,
        max_tokens=500
    )
    return message.content[0].text


def main():
    system_message = "You are an assistant that is great at telling jokes"
    user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"

    prompts = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]

    # GPT-4o-mini
    completion = openai.chat.completions.create(model='gpt-4o-mini', messages=prompts)
    print(completion.choices[0].message.content)

    # GPT-4.1-mini
    # Temperature setting controls creativity

    completion = openai.chat.completions.create(
        model='gpt-4.1-mini', 
        messages=prompts,
        temperature=0.7
    )
    print(completion.choices[0].message.content)

    # This is trained to think through its response before replying
    # So it will take longer but the answer should be more reasoned - not that this helps..

    completion = openai.chat.completions.create(
        model='o3-mini',
        messages=prompts
    )
    print(completion.choices[0].message.content)


    # Claude 3.7 Sonnet
    # API needs system message provided separately from user prompt
    # Also adding max_tokens

    message = claude.messages.create(
        model="claude-3-7-sonnet-latest",
        max_tokens=200,
        temperature=0.7,
        system=system_message,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )

    print(message.content[0].text)



    # Claude 3.7 Sonnet again
    # Now let's add in streaming back results
    # If the streaming looks strange, then please see the note below this cell!

    result = claude.messages.stream(
        model="claude-3-7-sonnet-latest",
        max_tokens=200,
        temperature=0.7,
        system=system_message,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )

    with result as stream:
        for text in stream.text_stream:
                print(text, end="", flush=True)



    # The API for Gemini has a slightly different structure.
    gemini = google.generativeai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=system_message
    )
    response = gemini.generate_content(user_prompt)
    print(response.text)


    # As an alternative way to use Gemini that bypasses Google's python API library,
    # Google released endpoints that means you can use Gemini via the client libraries for OpenAI!

    gemini_via_openai_client = OpenAI(
        api_key=google_api_key, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = gemini_via_openai_client.chat.completions.create(
        model="gemini-2.5-flash-preview-04-17",
        messages=prompts
    )
    print(response.choices[0].message.content)


    # Deepseek

    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

    if deepseek_api_key:
        print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
    else:
        print("DeepSeek API Key not set - please skip to the next section if you don't wish to try the DeepSeek API")

    # Using DeepSeek Chat

    deepseek_via_openai_client = OpenAI(
        api_key=deepseek_api_key, 
        base_url="https://api.deepseek.com"
    )

    response = deepseek_via_openai_client.chat.completions.create(
        model="deepseek-chat",
        messages=prompts,
    )

    print(response.choices[0].message.content)




    # Let's make a conversation between GPT-4o-mini and Gemini

    gpt_model = "gpt-4o-mini"
    claude_model = "claude-3-haiku-20240307"

    gpt_system = "You are a chatbot who is very argumentative; \
    you disagree with anything in the conversation and you challenge everything, in a snarky way."

    claude_system = "You are a very polite, courteous chatbot. You try to agree with \
    everything the other person says, or find common ground. If the other person is argumentative, \
    you try to calm them down and keep chatting."

    gemini_system = "You are a very polite, courteous chatbot. You try to agree with \
    everything the other person says, or find common ground. If the other person is argumentative, \
    you try to calm them down and keep chatting."

    gpt_messages = ["Hi there"]
    gemini_messages = ["Hi"]
    claude_messages = ["Hi"]

    # Testing all three models
    call_gpt(gpt_model, gpt_system, gpt_messages, gemini_messages)
    call_gemini(gpt_messages, gemini_messages, gemini_system)
    call_claude(gpt_messages, claude_messages, claude_model, claude_system)


    # creating chat between gpt and gemini
    gpt_messages = ["Hi there"]
    gemini_messages = ["Hi"]

    print(f"GPT:\n{gpt_messages[0]}\n")
    print(f"Gemini:\n{gemini_messages[0]}\n")

    for i in range(5):
        gpt_next = call_gpt()
        print(f"GPT:\n{gpt_next}\n")
        gpt_messages.append(gpt_next)
        
        gemini_next = call_gemini()
        print(f"Gemini:\n{gemini_next}\n")
        gemini_messages.append(gemini_next)