from src.decision import calculateConfidence, generateRefusalMessage
from src.llm import generateAnswer as generateLlmAnswer



def generateAnswer(question, retrievedChunks, similarityScores, threshold=0.4):
    """
    Generates an answer if confident, otherwise refuses.
    retrievedChunks: list of text chunks
    similarityScores: distances from FAISS
    """

    # Step 1: Confidence gate (authoritative)
    confident, score = calculateConfidence(similarityScores, threshold)
    if not confident:
        return generateRefusalMessage()

    # Step 2: Prepare context for LLM (controlled)
    contextChunks = []
    for i, chunk in enumerate(retrievedChunks):
        contextChunks.append({
            "id": f"Source {i+1}",
            "text": chunk.strip()
        })

    # Step 3: LLM generation (non-authoritative)
    answer = generateLlmAnswer(
        contextChunks=contextChunks,
        question=question
    )

    return answer


if __name__ == "__main__":
    # Example test
    testChunks = ["Chunk 1 content about AI.", "Chunk 2 content about RAG."]
    testDistances = [0.1, 0.2]  # example similarity distances
    question = "What is hallucination-resistant RAG?"

    answer = generateAnswer(question, testChunks, testDistances)
    print(answer)
