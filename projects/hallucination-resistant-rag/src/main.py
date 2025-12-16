import os
import sys
from pathlib import Path

# Get the project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent

# Add project root to Python path so imports work
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chunk import chunkText
from src.embed import createEmbedding, embedChunks
from src.generate import generateAnswer
from src.ingest import ingestDocuments
from src.retrieve import buildFaissIndex, searchFaiss


def runRAGForSingleFile(session_id: str):
    """
    Processes a single uploaded PDF file for a given session.
    """
    session_dir = PROJECT_ROOT / "data" / "sessions" / session_id
    uploads_dir = session_dir / "uploads"
    embeddings_dir = session_dir / "embeddings"
    chunks_dir = session_dir / "chunks"
    index_dir = session_dir / "index"

    for d in [embeddings_dir, chunks_dir, index_dir]:
        d.mkdir(exist_ok=True)

    # Ingest the document
    documents = ingestDocuments(str(uploads_dir))
    if not documents:
        raise Exception("No document found in the session's upload directory.")

    # Chunk and embed
    for file_name, text in documents.items():
        chunk_list = chunkText(text)
        embedChunks(chunk_list, file_name, embeddings_dir)

    # Build FAISS index
    buildFaissIndex(str(embeddings_dir), str(index_dir))


def runRAGSystem(question, session_id=None, threshold=0.25, topK=3):
    if session_id:
        session_dir = PROJECT_ROOT / "data" / "sessions" / session_id
        docs_folder = str(session_dir / "uploads")
        embeddings_root = session_dir / "embeddings"
        index_dir = session_dir / "index"
    else:
        # Default behavior
        docs_folder = str(PROJECT_ROOT / "data" / "documents")
        embeddings_root = PROJECT_ROOT / "embeddings"
        index_dir = embeddings_root  # Assuming index is stored with embeddings

    # Step 1: Ingest documents (to get text for context)
    documents = ingestDocuments(docs_folder)
    if not documents:
        return "No documents found. Please upload a PDF."

    # Step 2: Build FAISS index path
    faiss_index_path = index_dir
    if not session_id:
        # Compatibility with old structure
        index, metadata = buildFaissIndex(str(embeddings_root))
    else:
        index, metadata = buildFaissIndex(str(embeddings_root), str(faiss_index_path))

    # Step 3: Create embedding for user question
    queryVector = createEmbedding(question)

    # Step 4: Retrieve topK chunks
    searchResults = searchFaiss(index, queryVector, metadata, topK=topK)

    # Step 5: Extract retrieved chunks and similarity scores
    retrievedChunks = []
    similarityScores = []
    for fileName, chunkId, distance in searchResults:
        # Use cached text from ingestion step
        text = documents[fileName]
        # Map chunkId back to text chunk
        chunkNum = int(chunkId.split("_")[1].split(".")[0])
        chunkList = chunkText(text)
        retrievedChunks.append(chunkList[chunkNum])
        similarityScores.append(distance)

    # Step 6: Generate answer or refusal
    answer = generateAnswer(question, retrievedChunks, similarityScores, threshold)
    return answer


import sys

if __name__ == "__main__":
    print("=== Hallucination-Resistant RAG System ===")
    if len(sys.argv) > 1:
        userQuestion = sys.argv[1]
        print(f"Question: {userQuestion}")
    else:
        userQuestion = input("Enter your question: ")

    response = runRAGSystem(userQuestion)
    print("\n=== Response ===")
    print(response)
