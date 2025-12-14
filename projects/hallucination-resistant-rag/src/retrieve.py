import os

import faiss
import numpy as np


def buildFaissIndex(embeddingFolder):
    """
    Build a FAISS index from all .npy embeddings in the given folder.
    Returns the index and a list of (fileName, chunkId) metadata.
    """
    vectors = []
    metadata = []

    for fileName in os.listdir(embeddingFolder):
        filePath = os.path.join(embeddingFolder, fileName)
        if os.path.isdir(filePath):
            for chunkFile in os.listdir(filePath):
                if chunkFile.endswith(".npy"):
                    vector = np.load(os.path.join(filePath, chunkFile))
                    if vector.ndim == 1:
                        vectors.append(vector)
                        metadata.append((fileName, chunkFile))
                    else:
                        print(f"Skipping invalid vector: {fileName}/{chunkFile}")

    if not vectors:
        raise ValueError("No embeddings found in embeddings folder!")

    vectors = np.stack(vectors).astype("float32")  # ensures 2D array
    dim = vectors.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    print(f"Index built with {index.ntotal} vectors")
    return index, metadata


def searchFaiss(index, queryVector, metadata, topK=3):
    """
    Search the FAISS index for the k most similar vectors to the query vector
    Returns a list of (filename, chunkId, score)
    """
    queryVector = np.array([queryVector]).astype("float32")
    distances, indices = index.search(queryVector, topK)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        results.append((metadata[idx][0], metadata[idx][1], dist))
    return results


if __name__ == "__main__":
    # Example test

    from src.embed import createEmbedding

    testVector = createEmbedding("This system avoids hallucinations.")
    index, metadata = buildFaissIndex("embedding")
    results = searchFaiss(index, testVector, metadata)
    print("Top results", results)
