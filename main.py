from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
import openai
import uuid
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

connection = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
)

connection.recreate_collection(
    collection_name="chatbot2",
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

timestamps = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class URL(BaseModel):
    url: str

class Question(BaseModel):
    question: str

def read_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = '\n'.join([para.get_text() for para in paragraphs])
        return text
    else:
        return ""

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1500,
        chunk_overlap=400,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_embedding(text_chunks, model_id="text-embedding-ada-002"):
    points = []
    for idx, chunk in enumerate(text_chunks):
        response = openai.Embedding.create(
            input=chunk,
            model=model_id
        )
        embeddings = response['data'][0]['embedding']
        point_id = str(uuid.uuid4()) 

        points.append(PointStruct(id=point_id, vector=embeddings, payload={"text": chunk}))

    return points

def insert_data(get_points):
    operation_info = connection.upsert(
        collection_name="chatbot2",
        wait=True,
        points=get_points
    )

def create_answer_with_context(query):
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']

    search_result = connection.search(
        collection_name="chatbot2",
        query_vector=embeddings,
        limit=1
    )

    prompt = "Context:\n"
    for result in search_result:
        prompt += result.payload['text'] + "\n---\n"
    prompt += "Question:" + query + "\n---\n" + "Answer:"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content

@app.get("/")
async def def_home():
    return {"message": f"Welcome to the Custom RAG Chatbot. Time {timestamps}"}

@app.post("/process_url/")
def process_url(url: URL):
    try:
        get_raw_text = read_data(url.url)
        chunks = get_text_chunks(get_raw_text)
        vectors = get_embedding(chunks)
        insert_data(vectors)
        return {"message": "Data processed and inserted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask_question/")
def ask_question(question: Question):
    try:
        answer = create_answer_with_context(question.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)