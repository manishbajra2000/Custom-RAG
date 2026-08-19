# RAG Backend

A production-style backend for document ingestion and conversational RAG, built with FastAPI.

The system allows users to:

- Upload PDF and TXT documents
- Extract and chunk document text
- Generate vector embeddings
- Store vectors in Qdrant
- Store document metadata in PostgreSQL
- Ask questions about uploaded documents
- Maintain multi-turn conversation history using Redis
- Contextualize follow-up questions
- Schedule interviews through natural language
- Store interview bookings in PostgreSQL

---

## Architecture

```text
                         ┌─────────────────────┐
                         │       Client        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │       REST API      │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐           ┌──────────────────┐
          │ Document Ingest  │           │   Chat Service   │
          └────────┬─────────┘           └────────┬─────────┘
                   │                              │
          ┌────────┴─────────┐          ┌────────┴─────────┐
          │                  │          │                  │
          ▼                  ▼          ▼                  ▼
    Text Extraction      Chunking    Redis             RAG Service
                              │       Memory                 │
                              │                              │
                              ▼                    ┌─────────┴─────────┐
                         Embeddings                │                   │
                              │                    ▼                   ▼
                              ▼                 Query             Qdrant
                           Qdrant             Contextualizer     Retrieval
                              │                    │                   │
                              └────────────────────┴─────────┬─────────┘
                                                             │
                                                             ▼
                                                          LLM
                                                             │
                                                             ▼
                                                          Answer

                    Interview Booking Flow
                              │
                              ▼
                    Booking Intent Detection
                              │
                              ▼
                    Booking Information
                         Extraction
                              │
                              ▼
                       Booking Parser
                              │
                              ▼
                      Booking Service
                              │
                              ▼
                         PostgreSQL
```

---

## Tech Stack

| Component | Technology |
|---|---|
| API | FastAPI |
| Language | Python 3.12 |
| LLM | Groq |
| Embeddings | Hugging Face embedding model |
| Vector Database | Qdrant |
| Relational Database | PostgreSQL |
| Chat Memory | Redis |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Containers | Docker Compose |
| Testing | Pytest |

---

# Features

## 1. Document Ingestion

The ingestion API accepts:

- `.pdf`
- `.txt`

The ingestion pipeline:

```text
File
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding Generation
 ↓
Qdrant
```

Document metadata is stored separately in PostgreSQL.

Stored metadata includes:

- Document ID
- Filename
- File type
- File size
- Chunking strategy
- Chunk count
- Creation timestamp

---

## 2. Chunking Strategies

The system supports multiple chunking strategies.

The selected strategy is provided when ingesting a document.

Chunking allows the system to retrieve relevant sections of a document instead of embedding and searching the entire document at once.

---

## 3. Vector Search

Each document chunk is converted into an embedding vector.

The vectors are stored in Qdrant together with the original chunk text.

During a query:

```text
User Question
     ↓
Question Embedding
     ↓
Qdrant Similarity Search
     ↓
Relevant Chunks
```

---

## 4. Conversational RAG

The chat API implements a custom RAG pipeline rather than using `RetrievalQAChain`.

The flow is:

```text
User Question
     ↓
Conversation History
     ↓
Query Contextualization
     ↓
Embedding
     ↓
Qdrant Retrieval
     ↓
Relevant Context
     ↓
LLM
     ↓
Answer
```

The LLM is instructed to answer using the retrieved document context.

If the answer cannot be found in the provided documents, the system responds:

```text
I couldn't find the answer in the provided documents.
```

---

## 5. Conversational Memory

Redis stores chat history for each session.

Example:

```text
chat:session:<session_id>
```

This allows the system to understand follow-up questions.

For example:

```text
User: What are the four houses at Hogwarts?

Assistant: Gryffindor, Hufflepuff, Ravenclaw, and Slytherin.

User: Just name two.

Assistant: Gryffindor and Hufflepuff.
```

The second question can be interpreted using the previous conversation.

---

## 6. Interview Booking

The chat API also supports interview booking through natural language.

Example:

```text
User:
I want to book an interview.

Assistant:
Sure. I need your name, email, date and time.

User:
My name is Manish.

User:
My email is manish@example.com.

User:
August 20, 2026.

User:
3 PM.
```

The booking pipeline is:

```text
User Message
     ↓
Booking Intent Detection
     ↓
Booking Extraction
     ↓
Redis Booking State
     ↓
Missing Field Detection
     ↓
Booking Parser
     ↓
Booking Service
     ↓
PostgreSQL
```

The booking information stored in PostgreSQL includes:

- Booking ID
- Name
- Email
- Interview date
- Interview time
- Creation timestamp

---

# Project Structure

```text
palm-mind-rag/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py
│   │       ├── documents.py
│   │       └── health.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── dependencies.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── booking.py
│   │   ├── chat.py
│   │   └── document.py
│   │
│   └── services/
│       ├── booking.py
│       ├── booking_extractor.py
│       ├── booking_parser.py
│       ├── chat.py
│       ├── chat_memory.py
│       ├── chunking.py
│       ├── document_extractor.py
│       ├── embeddings.py
│       ├── ingestion.py
│       ├── llm.py
│       ├── qdrant.py
│       ├── query_contextualizer.py
│       ├── rag.py
│       └── redis.py
│
├── tests/
│   ├── test_booking.py
│   ├── test_booking_extractor.py
│   ├── test_booking_parser.py
│   ├── test_booking_flow.py
│   ├── test_booking_intent.py
│   ├── test_chat_memory.py
│   ├── test_contextualizer.py
│   ├── test_llm.py
│   ├── test_rag.py
│   └── test_redis.py
│
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# Requirements

Make sure the following are installed:

- Python 3.12
- Docker
- Docker Compose
- Git

---

# Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd palm-mind-rag
```

Create and activate the Conda environment:

```bash
conda create -n palm-mind python=3.12
conda activate palm-mind
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

Add any other provider credentials required by the configured services.

Do not commit `.env` or API keys to GitHub.

---

# Start Infrastructure

Start PostgreSQL, Qdrant and Redis:

```bash
docker compose up -d
```

Check the containers:

```bash
docker compose ps
```

You should see:

```text
postgres   Up
qdrant     Up
redis      Up
```

---

# Run the API

Start FastAPI:

```bash
fastapi dev app/main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Health Check

```http
GET /health
```

---

## Document Ingestion

```http
POST /documents/ingest
```

Accepts a PDF or TXT file and stores the processed document.

Example response:

```json
{
  "document_id": "cd28d89a-a5b1-46d2-b466-d5059f5de189",
  "filename": "harrypotter.txt",
  "chunking_strategy": "recursive",
  "chunks_created": "662"
}
```

---

## Chat

```http
POST /chat
```

Request:

```json
{
  "session_id": "demo-session",
  "message": "What are the four houses at Hogwarts?"
}
```

Response:

```json
{
  "session_id": "demo-session",
  "answer": "The four houses at Hogwarts are called Gryffindor, Hufflepuff, Ravenclaw, and Slytherin."
}
```

---

# Testing

Run the complete test suite:

```bash
pytest
```

Individual component tests can also be run directly:

```bash
python test_redis.py
python test_chat_memory.py
python test_llm.py
python test_rag.py
python test_contextualizer.py
python test_booking_intent.py
python test_booking_extractor.py
python test_booking_parser.py
python test_booking.py
```

---

# Database Services

The project uses Dockerized infrastructure.

### PostgreSQL

Default port:

```text
5432
```

Used for:

- Document metadata
- Interview bookings

### Qdrant

Default port:

```text
6333
```

Used for:

- Document chunk embeddings
- Vector similarity search

### Redis

Default port:

```text
6379
```

Used for:

- Chat history
- Temporary booking state

---

# Design Decisions

## Why Qdrant?

Qdrant provides vector similarity search suitable for semantic retrieval in RAG applications.

## Why PostgreSQL?

Relational data such as document metadata and interview bookings is structured and benefits from transactional persistence.

## Why Redis?

Conversation history and temporary booking state require fast access and are naturally represented as session-based data.

## Why custom RAG?

The task requires a custom RAG implementation rather than using `RetrievalQAChain`. The retrieval and generation steps are therefore explicitly controlled by the application.

## Why contextualize queries?

Follow-up questions such as:

```text
Which one is Harry in?
```

depend on previous conversation context.

The contextualizer transforms them into standalone queries such as:

```text
Which Hogwarts house is Harry in?
```

before performing retrieval.

---

# Error Handling

The application validates:

- File type
- File content
- Booking fields
- Email format
- Interview date
- Interview time
- Required request fields

The booking extractor also handles LLM responses wrapped in Markdown JSON code fences.

---

# Security Notes

API keys and credentials should be stored in environment variables.

The `.env` file should never be committed.

Generated Python bytecode and cache directories are excluded through `.gitignore`.

---

# Running the Full System

A typical development session:

```bash
# Activate environment
conda activate palm-mind

# Start infrastructure
docker compose up -d

# Start API
fastapi dev app/main.py
```

Then open:

```text
http://127.0.0.1:8000/docs
```

---

# End-to-End Flow

### Document ingestion

```text
PDF/TXT
  ↓
Text Extraction
  ↓
Chunking
  ↓
Embeddings
  ↓
Qdrant
  +
PostgreSQL Metadata
```

### Conversational RAG

```text
Question
  ↓
Redis Conversation History
  ↓
Query Contextualization
  ↓
Embedding
  ↓
Qdrant Retrieval
  ↓
LLM
  ↓
Answer
  ↓
Redis Conversation History
```

### Interview booking

```text
Booking Request
  ↓
Intent Detection
  ↓
Information Extraction
  ↓
Redis Booking State
  ↓
Missing Field Check
  ↓
Parser / Validation
  ↓
Booking Service
  ↓
PostgreSQL
```

---

# Project Status

The core backend implementation is complete and has been tested end-to-end.

Implemented:

- Document ingestion
- PDF/TXT extraction
- Configurable chunking
- Embedding generation
- Qdrant vector search
- PostgreSQL metadata storage
- Custom conversational RAG
- Redis conversation memory
- Query contextualization
- Interview intent detection
- Natural-language booking extraction
- Booking validation
- PostgreSQL booking persistence
- Multi-turn booking flow
- Dockerized infrastructure
- Automated/component testing

---

# Author

MANISH HARSHA BAJRACHARYA

Built as part of the Palm Mind AI hiring task.
