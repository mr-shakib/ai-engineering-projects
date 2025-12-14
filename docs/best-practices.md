# Best Practices for AI Engineering

This guide outlines best practices for building production-quality AI systems in this monorepo.

## Code Quality

### 1. Type Hints

Always use type hints for function signatures:

```python
from typing import List, Dict, Optional, Union, Tuple

def process_documents(
    documents: List[str],
    max_length: int = 1000,
    metadata: Optional[Dict[str, Any]] = None
) -> Tuple[List[str], Dict[str, int]]:
    """Process documents with type-safe interface."""
    pass
```

### 2. Docstrings

Use Google-style docstrings:

```python
def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """Generate embedding vector for input text.
    
    Args:
        text: Input text to embed. Should be preprocessed and cleaned.
        model: Name of the embedding model to use.
        
    Returns:
        List of floats representing the embedding vector.
        
    Raises:
        ValueError: If text is empty or None.
        APIError: If the embedding API call fails.
        
    Examples:
        >>> embed_text("Hello world")
        [0.1, 0.2, ..., 0.9]
    """
```

### 3. Error Handling

Be specific with exceptions:

```python
# Bad
try:
    result = api_call()
except Exception as e:
    print(f"Error: {e}")
    return None

# Good
from custom_exceptions import APIError, RateLimitError

try:
    result = api_call()
except RateLimitError as e:
    logger.warning(f"Rate limit hit: {e}. Retrying...")
    time.sleep(60)
    result = api_call()
except APIError as e:
    logger.error(f"API error: {e}")
    raise
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise
```

### 4. Logging

Use structured logging:

```python
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

# Bad
print(f"Processing {len(docs)} documents")

# Good
logger.info(
    json.dumps({
        "event": "document_processing_started",
        "timestamp": datetime.utcnow().isoformat(),
        "document_count": len(docs),
        "batch_id": batch_id
    })
)
```

## LLM Best Practices

### 1. Prompt Engineering

Structure prompts clearly:

```python
def create_rag_prompt(context: str, query: str) -> str:
    """Create a well-structured RAG prompt."""
    return f"""You are a helpful AI assistant. Answer the question based on the provided context.

Context:
{context}

Question: {query}

Instructions:
- Only use information from the context above
- If the context doesn't contain the answer, say "I don't have enough information"
- Be concise and specific
- Cite relevant parts of the context

Answer:"""
```

### 2. Temperature Settings

Choose appropriate temperature:

```python
# For factual, deterministic outputs
llm = ChatOpenAI(temperature=0.0)

# For creative generation
llm = ChatOpenAI(temperature=0.8)

# For balanced responses
llm = ChatOpenAI(temperature=0.3)
```

### 3. Token Management

Monitor and control token usage:

```python
from tiktoken import encoding_for_model

def estimate_tokens(text: str, model: str = "gpt-4") -> int:
    """Estimate token count for text."""
    encoding = encoding_for_model(model)
    return len(encoding.encode(text))

def truncate_context(
    context: str,
    max_tokens: int,
    model: str = "gpt-4"
) -> str:
    """Truncate context to fit within token limit."""
    encoding = encoding_for_model(model)
    tokens = encoding.encode(context)
    
    if len(tokens) <= max_tokens:
        return context
    
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)
```

### 4. Response Validation

Validate LLM outputs:

```python
def validate_response(
    response: str,
    context: str,
    query: str
) -> Tuple[bool, Optional[str]]:
    """Validate LLM response for quality and relevance.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check for common hallucination patterns
    if "I don't have" in response or "not mentioned" in response:
        return True, None
    
    # Check response length
    if len(response) < 10:
        return False, "Response too short"
    
    # Check for context grounding
    response_lower = response.lower()
    context_lower = context.lower()
    
    # Extract key phrases from response
    # Verify they appear in context
    
    return True, None
```

## Embedding Best Practices

### 1. Batch Processing

Process embeddings in batches:

```python
def batch_embed(
    texts: List[str],
    batch_size: int = 100
) -> List[List[float]]:
    """Embed texts in batches for efficiency."""
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = embedding_model.embed_documents(batch)
        embeddings.extend(batch_embeddings)
    
    return embeddings
```

### 2. Normalization

Normalize embeddings when needed:

```python
import numpy as np

def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize embedding to unit length."""
    embedding_array = np.array(embedding)
    norm = np.linalg.norm(embedding_array)
    
    if norm == 0:
        return embedding
    
    return (embedding_array / norm).tolist()
```

### 3. Dimension Reduction

Consider dimension reduction for efficiency:

```python
from sklearn.decomposition import PCA

def reduce_dimensions(
    embeddings: np.ndarray,
    target_dim: int = 256
) -> np.ndarray:
    """Reduce embedding dimensions using PCA."""
    pca = PCA(n_components=target_dim)
    return pca.fit_transform(embeddings)
```

## RAG Best Practices

### 1. Chunking Strategy

Choose appropriate chunk size:

```python
def chunk_document(
    text: str,
    chunk_size: int = 512,
    overlap: int = 50,
    preserve_sentences: bool = True
) -> List[str]:
    """Chunk document with smart boundaries."""
    if preserve_sentences:
        # Split on sentence boundaries
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence.split())
            
            if current_length + sentence_length > chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    # Keep last N words for overlap
                    overlap_words = current_chunk[-overlap:] if overlap > 0 else []
                    current_chunk = overlap_words
                    current_length = len(overlap_words)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    else:
        # Simple word-based chunking
        words = text.split()
        return [
            " ".join(words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size - overlap)
        ]
```

### 2. Retrieval Strategy

Implement hybrid retrieval:

```python
def hybrid_retrieval(
    query: str,
    vector_store,
    bm25_index,
    k: int = 5,
    alpha: float = 0.5
) -> List[Document]:
    """Combine vector and keyword search."""
    # Vector search
    vector_results = vector_store.similarity_search(query, k=k*2)
    
    # BM25 keyword search
    bm25_results = bm25_index.get_top_n(query, k=k*2)
    
    # Combine and rerank
    all_results = {}
    
    for i, doc in enumerate(vector_results):
        score = (k*2 - i) / (k*2)  # Normalized rank score
        all_results[doc.page_content] = {
            "doc": doc,
            "vector_score": score
        }
    
    for i, doc in enumerate(bm25_results):
        score = (k*2 - i) / (k*2)
        if doc.page_content in all_results:
            all_results[doc.page_content]["bm25_score"] = score
        else:
            all_results[doc.page_content] = {
                "doc": doc,
                "bm25_score": score,
                "vector_score": 0
            }
    
    # Weighted combination
    for content, data in all_results.items():
        vector_score = data.get("vector_score", 0)
        bm25_score = data.get("bm25_score", 0)
        data["final_score"] = alpha * vector_score + (1 - alpha) * bm25_score
    
    # Sort by final score
    sorted_results = sorted(
        all_results.values(),
        key=lambda x: x["final_score"],
        reverse=True
    )
    
    return [item["doc"] for item in sorted_results[:k]]
```

### 3. Context Window Management

Optimize context usage:

```python
def build_context(
    retrieved_docs: List[Document],
    query: str,
    max_tokens: int = 4000
) -> str:
    """Build context from retrieved documents within token limit."""
    context_parts = []
    total_tokens = 0
    
    # Reserve tokens for system prompt and query
    reserved_tokens = estimate_tokens(SYSTEM_PROMPT) + estimate_tokens(query)
    available_tokens = max_tokens - reserved_tokens - 500  # Buffer
    
    for doc in retrieved_docs:
        doc_tokens = estimate_tokens(doc.page_content)
        
        if total_tokens + doc_tokens <= available_tokens:
            context_parts.append(doc.page_content)
            total_tokens += doc_tokens
        else:
            # Truncate last document if needed
            remaining_tokens = available_tokens - total_tokens
            if remaining_tokens > 100:  # Minimum useful size
                truncated = truncate_context(
                    doc.page_content,
                    remaining_tokens
                )
                context_parts.append(truncated)
            break
    
    return "\n\n".join(context_parts)
```

## Testing Best Practices

### 1. Mock External APIs

```python
from unittest.mock import Mock, patch
import pytest

@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls."""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {
            'choices': [{
                'message': {
                    'content': 'Mocked response'
                }
            }]
        }
        yield mock

def test_generate_with_mock(mock_openai):
    """Test generation with mocked API."""
    result = generate_response("test query")
    assert result == "Mocked response"
    assert mock_openai.called
```

### 2. Test Edge Cases

```python
def test_empty_input():
    """Test handling of empty input."""
    with pytest.raises(ValueError, match="Input cannot be empty"):
        process_text("")

def test_very_long_input():
    """Test handling of extremely long input."""
    long_text = "word " * 100000
    result = process_text(long_text)
    assert len(result) < MAX_OUTPUT_LENGTH

def test_special_characters():
    """Test handling of special characters."""
    special_text = "Test with émojis 🚀 and spëcial çhars"
    result = process_text(special_text)
    assert result is not None
```

### 3. Performance Tests

```python
import time

def test_embedding_performance():
    """Test embedding generation performance."""
    texts = ["test text"] * 1000
    
    start_time = time.time()
    embeddings = batch_embed(texts, batch_size=100)
    elapsed = time.time() - start_time
    
    assert len(embeddings) == 1000
    assert elapsed < 30  # Should complete in under 30 seconds
```

## Security Best Practices

### 1. API Key Management

```python
import os
from typing import Optional

def get_api_key(key_name: str) -> str:
    """Safely retrieve API key from environment."""
    key = os.getenv(key_name)
    
    if key is None:
        raise ValueError(
            f"{key_name} not found in environment variables. "
            f"Please set it in your .env file."
        )
    
    return key

# Usage
OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")
```

### 2. Input Sanitization

```python
import re
from html import escape

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Escape HTML
    text = escape(text)
    
    # Limit length
    max_length = 10000
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()
```

### 3. Rate Limiting

```python
from functools import wraps
import time
from collections import deque

class RateLimiter:
    """Simple rate limiter using sliding window."""
    
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove old calls outside time window
            while self.calls and self.calls[0] < now - self.time_window:
                self.calls.popleft()
            
            # Check if rate limit exceeded
            if len(self.calls) >= self.max_calls:
                sleep_time = self.time_window - (now - self.calls[0])
                raise Exception(
                    f"Rate limit exceeded. Retry in {sleep_time:.2f}s"
                )
            
            # Record this call
            self.calls.append(now)
            
            return func(*args, **kwargs)
        
        return wrapper

# Usage
@RateLimiter(max_calls=10, time_window=60)
def call_api(query: str) -> str:
    """API call with rate limiting."""
    pass
```

## Performance Optimization

### 1. Caching

```python
from functools import lru_cache
import hashlib
import pickle

class EmbeddingCache:
    """Persistent cache for embeddings."""
    
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_key(self, text: str) -> str:
        """Generate cache key from text."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def get(self, text: str) -> Optional[List[float]]:
        """Retrieve cached embedding."""
        key = self._get_key(text)
        cache_file = self.cache_dir / f"{key}.pkl"
        
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        return None
    
    def set(self, text: str, embedding: List[float]):
        """Cache an embedding."""
        key = self._get_key(text)
        cache_file = self.cache_dir / f"{key}.pkl"
        
        with open(cache_file, 'wb') as f:
            pickle.dump(embedding, f)
```

### 2. Async Processing

```python
import asyncio
from typing import List

async def async_embed_batch(texts: List[str]) -> List[List[float]]:
    """Embed texts asynchronously."""
    tasks = [embed_single_async(text) for text in texts]
    return await asyncio.gather(*tasks)

async def embed_single_async(text: str) -> List[float]:
    """Async embedding for single text."""
    # Implementation with async API call
    pass
```

## Documentation

### 1. README Structure

Every project should have:

```markdown
# Project Name

Brief description

## Features

- Feature 1
- Feature 2

## Installation

Step-by-step setup

## Usage

Code examples

## Architecture

High-level design

## API Reference

Detailed API docs

## Contributing

How to contribute

## License

License info
```

### 2. Code Comments

```python
# Good comments explain WHY, not WHAT
def calculate_similarity(vec1, vec2):
    # Use cosine similarity instead of Euclidean distance
    # because it's invariant to vector magnitude, making it
    # more robust for embeddings of different lengths
    return cosine_similarity(vec1, vec2)
```

## Continuous Improvement

1. **Code Reviews** - All changes go through review
2. **Refactoring** - Regularly improve code quality
3. **Performance Monitoring** - Track metrics over time
4. **Learning** - Stay updated on AI/ML best practices
5. **Documentation** - Keep docs current

---

Remember: These are guidelines, not rigid rules. Use judgment to apply them appropriately to your specific use case.
