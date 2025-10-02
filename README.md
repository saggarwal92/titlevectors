# Title Vectors API

A simple FastAPI application for document indexing and searching.

## Project Structure

```
titlevectors/
├── routes/                 # API route handlers
│   ├── __init__.py
│   └── index_routes.py    # Index and search endpoints
├── services/              # Business logic
│   ├── __init__.py
│   └── index_service.py   # Index management service
├── models.py              # Pydantic models
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Create Index
- **POST** `/api/v1/create_index`
- Creates or initializes the search index
- No request body required

### 2. Index Document
- **POST** `/api/v1/index`
- Indexes a document with its content and metadata
- Request body:
```json
{
  "doc_id": "string",
  "search_content": "string",
  "metadata": {
    "key": "value"
  }
}
```

### 3. Search Documents
- **POST** `/api/v1/search`
- Searches for documents based on search content
- Request body:
```json
{
  "search_content": "string"
}
```

## API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## Example Usage

1. First, create the index:
```bash
curl -X POST "http://localhost:8000/api/v1/create_index"
```

2. Index a document:
```bash
curl -X POST "http://localhost:8000/api/v1/index" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "doc1",
    "search_content": "This is a sample document about machine learning",
    "metadata": {"category": "AI", "author": "John Doe"}
  }'
```

3. Search for documents:
```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "search_content": "machine learning"
  }'
```

## Features

- Simple in-memory document storage (for demonstration)
- Basic text-based search functionality
- RESTful API design
- Automatic API documentation with Swagger/OpenAPI
- Error handling and validation
- Modular architecture with separation of concerns