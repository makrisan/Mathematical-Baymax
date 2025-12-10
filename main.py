"""
FastAPI Backend for RAG System
Provides /chat endpoint for question answering using ChromaDB and Ollama
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os

# Configuration
DB_DIR = "chroma_db"
COLLECTION_NAME = "pdf_documents"
TOP_K = 3  # Number of relevant chunks to retrieve
MODEL_NAME = "llama2"  # Ollama model to use

# Initialize FastAPI app
app = FastAPI(title="Mathematical Baymax RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize models and DB (lazy loading)
embedding_model = None
chroma_client = None
collection = None


def get_embedding_model():
    """Lazy load embedding model"""
    global embedding_model
    if embedding_model is None:
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return embedding_model


def get_collection():
    """Lazy load ChromaDB collection"""
    global chroma_client, collection
    if collection is None:
        if not os.path.exists(DB_DIR):
            raise HTTPException(
                status_code=500,
                detail="Vector database not found. Please run ingest.py first."
            )
        chroma_client = chromadb.PersistentClient(path=DB_DIR)
        try:
            collection = chroma_client.get_collection(name=COLLECTION_NAME)
        except:
            raise HTTPException(
                status_code=500,
                detail=f"Collection '{COLLECTION_NAME}' not found. Please run ingest.py first."
            )
    return collection


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
async def root():
    """Serve the frontend HTML"""
    return FileResponse("static/index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    RAG endpoint: retrieves relevant chunks and generates answer using Ollama
    """
    try:
        # Get models and collection
        model = get_embedding_model()
        coll = get_collection()
        
        # Generate query embedding
        query_embedding = model.encode(request.question).tolist()
        
        # Retrieve relevant chunks
        results = coll.query(
            query_embeddings=[query_embedding],
            n_results=TOP_K
        )
        
        if not results['documents'] or not results['documents'][0]:
            return ChatResponse(
                answer="I don't have enough information to answer that question. Please add relevant PDF documents.",
                sources=[]
            )
        
        # Extract retrieved chunks and sources
        chunks = results['documents'][0]
        metadatas = results['metadatas'][0]
        sources = [meta['source'] for meta in metadatas]
        
        # Build context from retrieved chunks
        context = "\n\n".join([f"[{i+1}] {chunk}" for i, chunk in enumerate(chunks)])
        
        # Build prompt for LLM
        prompt = f"""You are a helpful assistant that answers questions based on the provided context. Use the context to answer the question accurately. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {request.question}

Answer:"""
        
        # Call Ollama API
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            
            answer = response['message']['content']
            
        except Exception as e:
            # If Ollama fails, provide a helpful error
            if "model" in str(e).lower() or "not found" in str(e).lower():
                return ChatResponse(
                    answer=f"Error: Ollama model '{MODEL_NAME}' not found. Please run 'ollama pull {MODEL_NAME}' first.",
                    sources=sources
                )
            raise HTTPException(
                status_code=500,
                detail=f"Ollama API error: {str(e)}"
            )
        
        return ChatResponse(
            answer=answer,
            sources=list(set(sources))  # Remove duplicates
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.get("/health")
async def health():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "db_exists": os.path.exists(DB_DIR),
        "collection_count": 0
    }
    
    try:
        coll = get_collection()
        status["collection_count"] = coll.count()
    except:
        pass
    
    return status


if __name__ == "__main__":
    import uvicorn
    print("Starting Mathematical Baymax RAG server...")
    print(f"Visit http://localhost:8000 to use the application")
    uvicorn.run(app, host="0.0.0.0", port=8000)
