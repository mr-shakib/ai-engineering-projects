import os
import json
import faiss
import numpy as np


def buildFaissIndex(embeddingFolder, index_dir=None):
    """
    Build a FAISS index from all .npy embeddings in the given folder.
    Saves the index and metadata, or loads them if they already exist.
    """
    if index_dir is None:
        index_dir = embeddingFolder

    index_file = os.path.join(index_dir, "faiss_index.bin")
    metadata_file = os.path.join(index_dir, "metadata.json")

    if os.path.exists(index_file) and os.path.exists(metadata_file):
        print(f"Loading existing index from {index_dir}")
        index = faiss.read_index(index_file)
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        return index, metadata

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

    vectors = np.stack(vectors).astype("float32")
    dim = vectors.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    print(f"Index built with {index.ntotal} vectors")

    # Save the index and metadata
    faiss.write_index(index, index_file)
    with open(metadata_file, "w") as f:
        json.dump(metadata, f)

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
