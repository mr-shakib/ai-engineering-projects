# Development Guidelines

**Personal Portfolio Repository**

This document outlines my development workflow and standards for maintaining high-quality AI Engineering projects.

## 🎯 Purpose

This repository showcases my AI Engineering skills through production-quality projects. I maintain strict development standards and best practices to ensure professional-grade code.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Git
- Familiarity with AI/ML concepts
- Understanding of the project you're contributing to

### Setting Up Your Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-engineering-projects.git
   cd ai-engineering-projects
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 📝 Personal Workflow

### 1. Project Planning

- Define clear project goals and success criteria
- Research best practices and architectural patterns
- Document design decisions
- Create implementation checklist

### 2. Branch Strategy

```bash
git checkout -b feature/project-name
git checkout -b fix/issue-description
```

Branch naming conventions:
- `feature/` - New features or projects
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code improvements
- `test/` - Adding tests
- `experiment/` - Experimental features

### 3. Make Your Changes

Follow our coding standards (see below) and ensure:
- Code is well-documented
- Tests are included
- Existing tests pass
- Code is formatted with Black

### 4. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git commit -m "feat: add semantic search capability"
git commit -m "fix: resolve embedding dimension mismatch"
git commit -m "docs: update RAG system architecture"
```

Commit message format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation only
- `style:` - Formatting, missing semicolons, etc.
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 5. Push and Review

```bash
git push origin feature/your-feature-name
```

Before merging:
- Review code changes
- Ensure all tests pass
- Verify documentation is updated
- Check code quality metrics
- Validate against project goals

## 💻 Coding Standards

### Python Style Guide

We follow PEP 8 with these tools:

- **Black** for code formatting (88 character line length)
- **Ruff** for linting
- **isort** for import sorting
- **mypy** for type checking

Run all checks:
```bash
black .
ruff check .
isort .
mypy .
```

### Code Quality Requirements

- **Type hints:** Use type annotations for function signatures
- **Docstrings:** Use Google-style docstrings for all public functions
- **Error handling:** Implement proper exception handling
- **Logging:** Use Python's logging module, not print statements
- **Testing:** Maintain >80% test coverage for new code

### Example Code Style

```python
from typing import List, Optional

import numpy as np
from langchain.embeddings import OpenAIEmbeddings


def generate_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100
) -> np.ndarray:
    """Generate embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed.
        model: Name of the embedding model to use.
        batch_size: Number of texts to process in each batch.
        
    Returns:
        NumPy array of shape (len(texts), embedding_dim) containing embeddings.
        
    Raises:
        ValueError: If texts list is empty.
        APIError: If the API call fails.
    """
    if not texts:
        raise ValueError("texts list cannot be empty")
        
    embeddings = OpenAIEmbeddings(model=model)
    
    try:
        vectors = embeddings.embed_documents(texts)
        return np.array(vectors)
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        raise
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests for a specific project
cd projects/your-project
pytest tests/

# Run with coverage
pytest --cov=src --cov-report=html
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use fixtures for common setup
- Mock external API calls

Example test:
```python
import pytest
from unittest.mock import Mock, patch

from src.embed import generate_embeddings


def test_generate_embeddings_success():
    """Test successful embedding generation."""
    texts = ["hello world", "test text"]
    
    with patch('src.embed.OpenAIEmbeddings') as mock_embeddings:
        mock_embeddings.return_value.embed_documents.return_value = [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ]
        
        result = generate_embeddings(texts)
        
        assert result.shape == (2, 3)
        assert mock_embeddings.called


def test_generate_embeddings_empty_input():
    """Test error handling for empty input."""
    with pytest.raises(ValueError, match="texts list cannot be empty"):
        generate_embeddings([])
```

## 📚 Documentation

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short one-line description.
    
    Longer description if needed. Explain what the function does,
    any important details, algorithms used, etc.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: When and why this is raised.
        TypeError: When and why this is raised.
        
    Examples:
        >>> function_name("test", 42)
        True
    """
```

### Documentation Files

When adding new features:
- Update relevant markdown files in `docs/`
- Update project README if applicable
- Add inline code comments for complex logic
- Include example usage

## 🏗️ Starting a New Project

When adding a new project to the portfolio:

1. **Create project structure**
   ```
   projects/your-project/
   ├── README.md
   ├── requirements.txt
   ├── .env.example
   ├── src/
   │   ├── __init__.py
   │   └── main.py
   ├── tests/
   │   ├── __init__.py
   │   └── test_main.py
   └── data/
       └── .gitkeep
   ```

2. **Create a comprehensive README**
   - Project description and goals
   - Architecture overview
   - Setup instructions
   - Usage examples
   - Tech stack details

3. **Add to main README**
   - Update the projects section
   - Add status badge
   - Link to project directory

4. **Include proper documentation**
   - API documentation
   - Architecture diagrams
   - Example outputs

## 🔍 Review Process

### What We Look For

- Code quality and readability
- Test coverage
- Documentation completeness
- Adherence to style guide
- No breaking changes (or clearly documented)

### Review Timeline

- Initial review: 2-3 business days
- Feedback implementation: As needed
- Final approval: 1-2 business days

### After Approval

- Squash and merge or rebase
- Delete feature branch
- Close related issues

## 🐛 Issue Tracking

Personal issue tracking approach:
- Document bugs and ideas in issues or notes
- Clear problem statements
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages and stack traces

## 💡 Feature Ideas

When planning new features:
- Define clear use case and value
- Research existing solutions
- Consider implementation complexity
- Document design decisions
- Plan testing strategy

## 📊 Progress Tracking

Use various tools:
- GitHub issues for tracking
- Project boards for organization
- Changelogs for history
- Documentation for learnings

## 🎓 Continuous Learning

This repository reflects my learning journey in AI Engineering:
- Experiment with new techniques
- Implement best practices
- Document lessons learned
- Iterate and improve continuously

---

This is a living document that evolves as I refine my development process. 🚀
