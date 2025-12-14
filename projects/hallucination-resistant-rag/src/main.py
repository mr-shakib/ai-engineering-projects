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


def runRAGSystem(question, docsFolder=None, threshold=0.25, topK=3):
    if docsFolder is None:
        docsFolder = str(PROJECT_ROOT / "data" / "documents")
    # Step 1: Ingest documents
    documents = ingestDocuments(docsFolder)
    if not documents:
        return "No documents found. Please add PDFs to data/documents/"

    # Step 2: Chunk documents & embed if not already embedded
    embeddings_root = PROJECT_ROOT / "embeddings"
    embeddings_root.mkdir(exist_ok=True)

    for fileName, text in documents.items():
        embedDir = str(embeddings_root / fileName)
        if not os.path.exists(embedDir):
            print(f"Generating embeddings for {fileName}...")
            chunkList = chunkText(text)
            embedChunks(
                chunkList, fileName
            )  # creates embeddings in embeddings/<fileName>
        else:
            print(f"Skipping embedding for {fileName} (already exists).")

    # Step 3: Build FAISS index
    index, metadata = buildFaissIndex(str(embeddings_root))

    # Step 4: Create embedding for user question
    queryVector = createEmbedding(question)

    # Step 5: Retrieve topK chunks
    searchResults = searchFaiss(index, queryVector, metadata, topK=topK)

    # Extract retrieved chunks and similarity scores
    retrievedChunks = []
    similarityScores = []
    for fileName, chunkId, distance in searchResults:
        chunkPath = os.path.join("embeddings", fileName, chunkId)
        vector = None  # not used for generation, just distances
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
