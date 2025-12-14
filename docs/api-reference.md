# API Reference

This document provides API reference for common utilities and patterns used across projects.

## Table of Contents

- [Embedding APIs](#embedding-apis)
- [LLM APIs](#llm-apis)
- [Vector Store APIs](#vector-store-apis)
- [Utility Functions](#utility-functions)

## Embedding APIs

### EmbeddingClient

Base class for embedding generation.

```python
class EmbeddingClient:
    """Client for generating text embeddings."""
    
    def __init__(
        self,
        provider: str = "openai",
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        """Initialize embedding client.
        
        Args:
            provider: Embedding provider (openai, cohere, huggingface)
            model: Model name
            api_key: API key (if not in environment)
        """
```

#### Methods

##### `embed_documents(texts: List[str]) -> List[List[float]]`

Embed multiple documents.

**Parameters:**
- `texts`: List of text strings to embed

**Returns:**
- List of embedding vectors

**Example:**
```python
client = EmbeddingClient()
embeddings = client.embed_documents(["Hello", "World"])
# Returns: [[0.1, 0.2, ...], [0.3, 0.4, ...]]
```

##### `embed_query(text: str) -> List[float]`

Embed a single query.

**Parameters:**
- `text`: Query text

**Returns:**
- Embedding vector

## LLM APIs

### LLMClient

Unified interface for LLM providers.

```python
class LLMClient:
    """Client for LLM inference."""
    
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """Initialize LLM client."""
```

#### Methods

##### `generate(prompt: str, system_prompt: Optional[str] = None) -> str`

Generate text from prompt.

##### `stream(prompt: str) -> Iterator[str]`

Stream generation token by token.

## Vector Store APIs

### VectorStore

Abstract base class for vector databases.

```python
class VectorStore(ABC):
    """Abstract vector store interface."""
    
    @abstractmethod
    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadata: Optional[List[Dict]] = None
    ) -> List[str]:
        """Add documents to store."""
        pass
```

## Utility Functions

### Text Processing

#### `chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]`

Split text into overlapping chunks.

#### `clean_text(text: str) -> str`

Clean and normalize text.

### Token Management

#### `count_tokens(text: str, model: str) -> int`

Count tokens in text for specific model.

---

For complete API documentation, see individual project READMEs.
