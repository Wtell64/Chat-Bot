#Step 0 - Create a new env and install dependencies
env\Scripts\activate

#Step 1 - Get Env variables
for bash
export $(grep -v '^#' .env | xargs)

for cmd 
set /p VAR_NAME=<.env

#Step 2 - Run Chroma to set up Chroma for Db
python add_docs.py

#Step 3
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload

#Step 4
streamlit run app.py

