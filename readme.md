A simple chatbot application that utilizes Retrieval-Augmented Generation (RAG) to personalize OpenAI’s GPT model.

This project was initially developed as a demo for a private professional project but has been made publicly available as an example implementation.

# Installation & Setup

## Step 0: Create and Activate a Virtual Environment
```
env\Scripts\activate  # Windows \
source env/bin/activate  # macOS/Linux
```
## Step 1: Load Environment Variables
```
export $(grep -v '^#' .env | xargs) # For Bash \
set /p VAR_NAME=<.env # For Windows CMD 
```
## Step 2: Set Up Chroma Database
```
python add_docs.py
```
## Step 3: Start the Backend
```
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```
## Step 4: Launch the Frontend
```
streamlit run app.py
```
