"""
PDF Ingestion Script for RAG System
Processes PDF files and stores chunk embeddings in ChromaDB
"""
import os
import sys
from pathlib import Path
from PyPDF2 import PdfReader
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Configuration
CHUNK_SIZE = 500  # characters per chunk
CHUNK_OVERLAP = 50  # overlap between chunks
PDF_DIR = "pdfs"
DB_DIR = "chroma_db"
COLLECTION_NAME = "pdf_documents"


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None


def ingest_pdfs():
    """Main ingestion function"""
    # Create PDF directory if it doesn't exist
    Path(PDF_DIR).mkdir(exist_ok=True)
    
    # Check if there are PDFs to process
    pdf_files = list(Path(PDF_DIR).glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{PDF_DIR}' directory.")
        print(f"Please add PDF files to the '{PDF_DIR}' folder and run again.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process...")
    
    # Initialize embedding model
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # Get or create collection
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
        print(f"Using existing collection '{COLLECTION_NAME}'")
    except:
        collection = client.create_collection(name=COLLECTION_NAME)
        print(f"Created new collection '{COLLECTION_NAME}'")
    
    # Process each PDF
    total_chunks = 0
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        
        # Extract text
        text = extract_text_from_pdf(pdf_file)
        if not text:
            continue
        
        # Chunk text
        chunks = chunk_text(text)
        print(f"  Created {len(chunks)} chunks")
        
        # Generate embeddings and store
        for i, chunk in enumerate(chunks):
            chunk_id = f"{pdf_file.stem}_chunk_{i}"
            
            # Generate embedding
            embedding = model.encode(chunk).tolist()
            
            # Store in ChromaDB
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    "source": pdf_file.name,
                    "chunk_index": i
                }],
                ids=[chunk_id]
            )
        
        total_chunks += len(chunks)
        print(f"  ✓ Ingested {len(chunks)} chunks from {pdf_file.name}")
    
    print(f"\n✓ Ingestion complete! Total chunks stored: {total_chunks}")
    print(f"Collection '{COLLECTION_NAME}' now contains {collection.count()} items")


if __name__ == "__main__":
    print("=" * 50)
    print("PDF Ingestion Script")
    print("=" * 50)
    ingest_pdfs()
