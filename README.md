# Custom RAG Chatbot

This project implements a custom Retrieval-Augmented Generation (RAG) chatbot using FastAPI, OpenAI, and Qdrant, with enhanced capabilities to extract and process data from both web URLs and PDF documents.

## What is RAG?

Retrieval Augmented Generation (RAG) is a hybrid approach that combines retrieval-based techniques with generative models to provide more accurate and contextually relevant answers. In this chatbot, the RAG framework works by retrieving information from a knowledge base (constructed from web URLs and PDFs) and then using OpenAI's GPT model to generate natural language responses.

## Features

- **Web Scraping and Text Processing**: Extracts meaningful text data from web pages for use in the chatbot's knowledge base.
- **PDF Text Extraction**: Supports extracting text from PDF documents to enrich the chatbot's knowledge base.
- **Vector Embedding Generation**: Uses OpenAI's text embeddings to convert extracted text into vector representations for efficient storage and retrieval.
- **Vector Storage and Retrieval**: Stores and retrieves vector embeddings using Qdrant, allowing the chatbot to find the most relevant information quickly.
- **Enhanced Question Answering**: Combines retrieved data with OpenAI's GPT model to generate contextually relevant answers that are grounded in the imported information.

## How Importing URLs and PDFs Helps

- **Expands Knowledge Base**: By allowing the import of both web URLs and PDFs, the chatbot can build a rich, diverse, and up-to-date knowledge base.
- **Improves Accuracy**: More relevant data leads to better retrieval, which in turn helps the generative model produce more precise and informative answers.
- **Supports Diverse Data Sources**: The ability to process information from both *online and offline* sources makes the chatbot adaptable to different use cases, including research, customer support, and more.

## Setup

1. Clone the repository
2. Install dependencies:
   
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `OPENAI_API_KEY`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`

## Usage

1. Start the server: `uvicorn main:app --reload`
2. Process a URL: Send a POST request to `/process_url/` with a JSON body containing the URL.
3. Process a PDF: Send a POST request to `/process_pdf/` with the PDF file uploaded as a form field.
4. Ask a question: Send a POST request to `/ask_question/` with a JSON body containing the question

## API Endpoints

- `GET /`: Welcome message
- `POST /process_url/`: Process and store data from a given URL
- `POST /process_pdf/`: Process and store data from a PDF file
- `POST /ask_question/`: Ask a question and get an AI-generated answer

## Dependencies

- FastAPI
- Pydantic
- Requests
- BeautifulSoup
- PyMuPDF
- Langchain
- OpenAI
- Qdrant

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
