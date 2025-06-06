# imports
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display


class Website:

    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)


# A function that writes a User Prompt that asks for summaries of websites:
def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


# See how this function creates exactly the format above
def messages_for(website, system_prompt):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]


# And now: call the OpenAI API. You will get very familiar with this!
def summarize(url, system_prompt):
    website = Website(url)
    messages = messages_for(website, system_prompt)
    payload = {
            "model": MODEL,
            "messages": messages,
            "stream": False
        }
    response = requests.post(
        OLLAMA_API, json=payload, headers=HEADERS,
    )
    return response.json()['message']['content']


# A function to display this nicely in the Jupyter output, using markdown
def display_summary(url, system_prompt):
    summary = summarize(url, system_prompt)
    display(Markdown(summary))


if __name__=='__main__':

    # Constants
    OLLAMA_API = "http://localhost:11434/api/chat"
    HEADERS = {"Content-Type": "application/json"}
    MODEL = "llama3.2"

    # Some websites need you to use proper headers when fetching them:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    # Define our system prompt
    system_prompt = "You are an assistant that analyzes the contents of a website \
    and provides a short summary, ignoring text that might be navigation related. \
    Respond in markdown."

    display_summary("https://cnn.com", system_prompt)

