# LLM Projects

# Instructions for Edit_resume_to_match_job

# 🧠 Resume Matcher Assistant

This Python project summarizes the content of a resume and generates a tailored resume based on a provided job description using OpenAI's GPT models.

---

## ✅ Features

- 📄 Reads resumes and job descriptions from `.docx` files
- 🧠 Uses GPT-4o-mini to summarize resumes and tailor them to job descriptions
- ✅ Checks and validates your OpenAI API key
- 🛠️ Outputs summaries and generated resumes for review

---

## 🔧 Requirements

## Make sure you have **Anaconda or Miniconda** installed. [Download Miniconda here](https://docs.conda.io/en/latest/miniconda.html)

## 🧪 Setup Instructions

### 1. Clone the repository (if applicable)

```bash
git clone https://github.com/your-username/resume-matcher.git
cd resume-matcher
```

### 2. Create a Conda environment & activate

```bash
conda env create -f environment.yml
conda activate llms

```

### 3. Install required Python packages

```
pip install -r requirements.txt
pip3 install python-docx
```

## 📄 Create a .env file

In the project root directory, create a .env file and add your OpenAI API key:

```ini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ Make sure it starts with sk-proj- and has no extra spaces.

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
