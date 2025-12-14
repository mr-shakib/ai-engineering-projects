from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

model = SentenceTransformer("all-MiniLM-L6-v2")


def createEmbedding(text: str):
    """
    Convert input text into a numerical embedding.
    """
    embedding = model.encode(text)
    return embedding


def embedChunks(chunks, filename):
    """
    Generate embeddings for a list of text chunks.
    Save each embedding as a .npy file in embeddings/<fileName>/
    """
    embeddings_root = PROJECT_ROOT / "embeddings"
    folderPath = embeddings_root / filename
    folderPath.mkdir(parents=True, exist_ok=True)

    for i, chunk in enumerate(chunks):
        vector = createEmbedding(chunk)
        np.save(str(folderPath / f"chunk_{i}.npy"), vector)
    print(f"Generated {len(chunks)} embeddings for {filename}")


if __name__ == "__main__":
    sampleChunks = ["This is a test chunk.", "Another test chunk."]
    embedChunks(sampleChunks, "sampleDoc")
