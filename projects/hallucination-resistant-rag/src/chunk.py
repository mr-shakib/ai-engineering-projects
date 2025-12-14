import re


def chunkText(text, chunkSize=300, overlap=50):
    """
    Splits text into chunks with specified chunk size and overlap.
    """

    # clean multiple spaces/newlines
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split(" ")

    # create chunks
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunkSize
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunkSize - overlap
    return chunks


if __name__ == "__main__":
    sampleText = "This is a sample text to test the chunking function. " * 100
    chunks = chunkText(sampleText, chunkSize=100, overlap=20)
    print("Number of chunks:", len(chunks))
    print("First chunk:", chunks[0][:100], "...")
