from src.decision import calculateConfidence, generateRefusalMessage


def generateAnswer(question, retrievedChunks, similarityScores, threshold=0.4):
    """
    Generates an answer if confident, otherwise refuses.
    retrievedChunks: list of text chunks
    similarityScores: distances from FAISS
    """
    confident, score = calculateConfidence(similarityScores, threshold)
    if not confident:
        return generateRefusalMessage()

    # Format chunks for better readability
    formatted_context = ""
    for i, chunk in enumerate(retrievedChunks):
        formatted_context += f"\n--- Source {i+1} ---\n{chunk.strip()}\n"

    # Simulate LLM generation for now
    answer = (
        f"### Retrieved Information:\n"
        f"{formatted_context}\n"
        f"--------------------------------------------------\n"
        f"System Note: This is raw context. Connect an LLM to generate a natural language summary."
    )

    return answer


if __name__ == "__main__":
    # Example test
    testChunks = ["Chunk 1 content about AI.", "Chunk 2 content about RAG."]
    testDistances = [0.1, 0.2]  # example similarity distances
    question = "What is hallucination-resistant RAG?"

    answer = generateAnswer(question, testChunks, testDistances)
    print(answer)
