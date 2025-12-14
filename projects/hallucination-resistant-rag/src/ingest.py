import os

import pdfplumber


def extractTextFromPdf(file_path: str) -> str:
    """
    Extracts text from a PDF file and returns as a single string.
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def ingestDocuments(folder_path: str) -> dict:
    """
    Reads all PDFs in a folder and returns a dictionary:
    { filename: text }
    """
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            documents[filename] = extractTextFromPdf(path)
    return documents


if __name__ == "__main__":

    docs_folder = os.path.join(os.getcwd(), "data", "documents")
    print("Looking for documents in:", docs_folder)
    docs = ingestDocuments(docs_folder)
    for fname, content in docs.items():
        print(f"{fname}: {len(content)} characters")
