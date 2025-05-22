# LLM Projects

# 🧠 Ollama_summarize_website: Website summarize Assistant

This Python project summarizes the content of a website using Ollama's models.

## ✅ Features

- 📄 Reads the content of a website based on the provided url
- 🧠 Uses Ollama to summarize the contents of the website
- 🛠️ Outputs summaries

---

# 🧠 OpenAI_edit_resume_to_watch_job: Resume Matcher Assistant

This Python project summarizes the content of a resume and generates a tailored resume based on a provided job description using OpenAI's GPT models.

## ✅ Features

- 📄 Reads resumes and job descriptions from `.docx` files
- 🧠 Uses GPT-4o-mini to summarize resumes and tailor them to job descriptions
- ✅ Checks and validates your OpenAI API key
- 🛠️ Outputs summaries and generated resumes for review

---

# 🔧 Requirements

## Make sure you have **Anaconda or Miniconda** installed. [Download Miniconda here](https://docs.conda.io/en/latest/miniconda.html)

## 🧪 Setup Instructions

### Part 1: Clone the Repo

This gets you a local copy of the code on your box.

1. **Install Git** if not already installed (it will be in most cases)

- Open Terminal (Applications > Utilities > Terminal)
- Type `git --version` If not installed, you'll be prompted to install it
- After the installation, you may need to open a new Terminal window to use it (or you might even need to restart)

2. **Navigate to your projects folder:**

If you have a specific folder for projects, navigate to it using the cd command. For example:
`cd ~/Documents/Projects`

If you don't have a projects folder, you can create one:

```
mkdir ~/Documents/Projects
cd ~/Documents/Projects
```

3. **Clone the repository:**

Enter this in the terminal in the Projects folder:

`git clone https://github.com/ed-donner/llm_engineering.git`

This creates a new directory `llm_engineering` within your Projects folder and downloads the code for the class. Do `cd llm_engineering` to go into it. This `llm_engineering` directory is known as the "project root directory".

### Part 2: Install Anaconda environment

If this Part 2 gives you any problems, there is an alternative Part 2B below that can be used instead.

1. **Install Anaconda:**

- Download Anaconda from https://docs.anaconda.com/anaconda/install/mac-os/
- Double-click the downloaded file and follow the installation prompts. Note that it takes up several GB and take a while to install, but it will be a powerful platform for you to use in the future.
- After installing, you'll need to open a fresh, new Terminal to be able to use it (and you might even need to restart).

2. **Set up the environment:**

- Open a **new** Terminal (Applications > Utilities > Terminal)
- Navigate to the "project root directory" using `cd ~/Documents/Projects/llm_engineering` (replace this path as needed with the actual path to the llm_engineering directory, your locally cloned version of the repo). Do `ls` and check you can see subdirectories for each week of the course.
- Create the environment: `conda env create -f environment.yml`
- Wait for a few minutes for all packages to be installed - in some cases, this can literally take 20-30 minutes if you've not used Anaconda before, and even longer depending on your internet connection. Important stuff is happening! If this runs for more than 1 hour 15 mins, or gives you other problems, please go to Part 2B instead.
- You have now built an isolated, dedicated AI environment for engineering LLMs, running vector datastores, and so much more! You now need to **activate** it using this command: `conda activate llms`

You should see `(llms)` in your prompt, which indicates you've activated your new environment.

3. **Start Jupyter Lab:**

- In the Terminal window, from within the `llm_engineering` folder, type: `jupyter lab`

...and Jupyter Lab should open up in a browser. If you've not seen Jupyter Lab before, I'll explain it in a moment! Now close the jupyter lab browser tab, and close the Terminal, and move on to Part 3.

### Part 3. Install required Python packages

```
pip install -r requirements.txt
pip3 install python-docx
```

## 🚀 Running the Script

Once setup is complete, run the script:

```
python your_script_name.py
```

You will be prompted to enter:

    The name of the resume file (e.g., resume.docx)

    The name of the job description file (e.g., job_description.docx)

The script will then:

    Summarize the resume

    Generate a tailored resume

    Display the results using markdown

## 📦 File Requirements

Ensure both your resume and job description are in .docx format and placed in the same directory as the script.

## ✅ Troubleshooting

    If your API key doesn’t work, check for typos or spaces.

    Restart the kernel or terminal if you get unexpected errors.

    Check file paths if the script can't find your resume or job description.
