import sqlite3
import os
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Embeddings
embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)

# SQLite Database Setup
conn = sqlite3.connect("docs.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS docs (id INTEGER PRIMARY KEY, text TEXT)")
conn.commit()

# Truncate table 

cursor.execute("DELETE FROM docs")
conn.commit()


# Add new documents
documents = [
    "Fullstack course id 40000 turkish liras",
    "AI course is currently full and the next course is in April 2026",
    "Our organization does not have an cyber security course"
]

for text in documents:
    cursor.execute("INSERT INTO docs (text) VALUES (?)", (text,))
    conn.commit()

# Save documents to ChromaDB
vectorstore = Chroma(persist_directory="./docs_db", embedding_function=embedding_function)
vectorstore.add_texts(documents)

print("Documents added and indexed successfully!")
