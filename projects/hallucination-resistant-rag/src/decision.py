def calculateConfidence(similarityScores, threshold=0.5):
    """
    Determine if the retrieved chunks are reliable enough.
    similarityScores: list of distances from FAISS (L2)
    threshold: max allowed distance to consider answer reliable
    Returns: (isConfident: bool, score: float)
    """

    if not similarityScores:
        return False, 0.0

    # Convert distances to similarity (smaller distance -> higher similarity)
    # For simplicity: similarity = 1 / (1 + distance)

    similarities = [1 / (1 + d) for d in similarityScores]
    avgSimilarity = sum(similarities) / len(similarities)

    isConfident = avgSimilarity >= threshold
    return isConfident, avgSimilarity


def generateRefusalMessage():
    return "I'm sorry, but I cannot provide an answer based on the information available on the document. Please provide more context or ask a different question."


if __name__ == "__main__":
    # Example Test

    testScores = [1.8984377, 1.911989, 3.4028235e38]
    confident, score = calculateConfidence(testScores, threshold=0.4)
    if confident:
        print("Answer can be generated. Confidence score : {score:.2f}")
    else:
        print("Refusal message:")
        print(generateRefusalMessage())
