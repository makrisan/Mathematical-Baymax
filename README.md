# Mathematical-Baymax 🤖

A local RAG (Retrieval-Augmented Generation) system where you can upload your school PDFs and get AI-powered answers to your questions. Baymax will heal your math deficiencies!

## Features

- 📚 **PDF Ingestion**: Automatically process and index PDF documents
- 🔍 **Semantic Search**: Find relevant information using vector embeddings
- 🤖 **Local LLM**: Uses Ollama for completely offline AI responses
- 💻 **Simple Interface**: Clean web UI for asking questions
- 🚀 **Fast & Lightweight**: Minimal dependencies, runs locally

## Architecture

- **Backend**: FastAPI (Python)
- **Frontend**: Simple HTML/JavaScript
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: Ollama (llama2)

## Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running
   - Install from: https://ollama.ai
   - Pull the llama2 model: `ollama pull llama2`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/makrisan/Mathematical-Baymax.git
cd Mathematical-Baymax
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running and has the llama2 model:
```bash
ollama pull llama2
```

## Usage

### Step 1: Add Your PDF Documents

Place your PDF files in the `pdfs/` directory:
```bash
mkdir -p pdfs
# Copy your PDF files to the pdfs/ directory
```

### Step 2: Ingest the PDFs

Run the ingestion script to process PDFs and create embeddings:
```bash
python ingest.py
```

This will:
- Extract text from all PDFs in the `pdfs/` folder
- Split text into manageable chunks
- Generate embeddings using Sentence Transformers
- Store everything in ChromaDB (in `chroma_db/` directory)

### Step 3: Start the Server

Launch the FastAPI backend:
```bash
python main.py
```

The server will start at `http://localhost:8000`

### Step 4: Use the Web Interface

1. Open your browser and go to: `http://localhost:8000`
2. Type your question in the input box
3. Click "Ask Baymax" or press Enter
4. Get AI-powered answers based on your documents!

## API Endpoints

### `POST /chat`

Ask a question and get an AI-generated answer.

**Request:**
```json
{
  "question": "What is the Pythagorean theorem?"
}
```

**Response:**
```json
{
  "answer": "The Pythagorean theorem states that...",
  "sources": ["textbook.pdf", "notes.pdf"]
}
```

### `GET /health`

Check the server status and database stats.

## Project Structure

```
Mathematical-Baymax/
├── main.py              # FastAPI backend server
├── ingest.py            # PDF ingestion script
├── requirements.txt     # Python dependencies
├── static/
│   └── index.html      # Frontend web interface
├── pdfs/               # Place your PDF files here
└── chroma_db/          # Vector database (auto-generated)
```

## Configuration

You can modify these settings in the respective files:

**ingest.py:**
- `CHUNK_SIZE`: Characters per chunk (default: 500)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)

**main.py:**
- `TOP_K`: Number of chunks to retrieve (default: 3)
- `MODEL_NAME`: Ollama model to use (default: "llama2")

## Troubleshooting

### "Ollama model not found"
Make sure Ollama is running and you've pulled the model:
```bash
ollama pull llama2
```

### "Vector database not found"
Run the ingestion script first:
```bash
python ingest.py
```

### No PDFs found
Make sure you have PDF files in the `pdfs/` directory.

## Advanced Usage

### Using a Different Ollama Model

Edit `main.py` and change the `MODEL_NAME` variable:
```python
MODEL_NAME = "mistral"  # or "codellama", "phi", etc.
```

Then pull the model:
```bash
ollama pull mistral
```

### Re-ingesting PDFs

To add new PDFs or update existing ones:
1. Add/update PDFs in the `pdfs/` folder
2. Run `python ingest.py` again
3. Restart the server

## Contributing

Feel free to open issues or submit pull requests!

## License

MIT License - feel free to use this project for your learning needs!
