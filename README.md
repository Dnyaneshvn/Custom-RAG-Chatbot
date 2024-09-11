# Custom RAG Chatbot

This project implements a custom Retrieval-Augmented Generation (RAG) chatbot using FastAPI, OpenAI, and Qdrant.

## Features

- Web scraping and text processing
- Vector embedding generation using OpenAI
- Vector storage and retrieval with Qdrant
- Question answering using OpenAI's GPT model

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables:
   - `OPENAI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`

## Usage

1. Start the server: `uvicorn main:app --reload`
2. Process a URL: Send a POST request to `/process_url/` with a JSON body containing the URL
3. Ask a question: Send a POST request to `/ask_question/` with a JSON body containing the question

## API Endpoints

- `GET /`: Welcome message
- `POST /process_url/`: Process and store data from a given URL
- `POST /ask_question/`: Ask a question and get an AI-generated answer

## Dependencies

- FastAPI
- Pydantic
- Requests
- BeautifulSoup
- Langchain
- OpenAI
- Qdrant
