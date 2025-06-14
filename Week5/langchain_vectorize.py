# imports

import os
import glob
from dotenv import load_dotenv
import gradio as gr

# imports for langchain
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter

MODEL = "gpt-4o-mini"
db_name = "vector_db"

# Load environment variables in a file called .env
load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')


# Read in documents using LangChain's loaders
# Take everything in all the sub-folders of our knowledgebase
folders = glob.glob("knowledge-base/*")

text_loader_kwargs = {'encoding': 'utf-8'}
# If that doesn't work, some Windows users might need to uncomment the next line instead
# text_loader_kwargs={'autodetect_encoding': True}

documents = []
for folder in folders:
    doc_type = os.path.basename(folder)
    loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    folder_docs = loader.load()
    for doc in folder_docs:
        doc.metadata["doc_type"] = doc_type
        documents.append(doc)

# reasonable chunck size. Chunk overlap to help with context building
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# check out all doc types
doc_types = set(chunk.metadata['doc_type'] for chunk in chunks)
print(f"Document types found: {', '.join(doc_types)}")


for chunk in chunks:
    if 'CEO' in chunk.page_content:
        print(chunk)
        print("_________")

