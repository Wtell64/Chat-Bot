from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Env variablelari alma
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key. Set it in the .env file.")

# OPEN AI ile baglanti kurma
chat_model = ChatOpenAI(model_name="gpt-4o", openai_api_key=OPENAI_API_KEY, max_tokens=250)

# Local db ile vector store yapma (RAG icin)
vectorstore = Chroma(persist_directory="./docs_db", embedding_function=OpenAIEmbeddings(model="text-embedding-ada-002"))
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3, "lambda_mult": 0.7})

# Template
TEMPLATE = """
Answer the following question:
{question}

To answer the question, use only the following context:
{context}

"""

prompt_template = PromptTemplate.from_template(TEMPLATE)

# RAG chaini yapma
chain = ({
    "context": retriever,
    "question": RunnablePassthrough()
} | prompt_template | chat_model | StrOutputParser())

# FastAPI ile endpoint yapma
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    question = request.message
    try:
        response = chain.invoke(question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with OpenAI: {str(e)}")
