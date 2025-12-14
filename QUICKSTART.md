# Quick Reference Guide

Essential commands and patterns for working with my AI Engineering Projects portfolio.

## Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/ai-engineering-projects.git
cd ai-engineering-projects

# Setup environment
python scripts/setup.py

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Create .env file
cp .env.example .env
# Edit .env with your API keys
```

## Common Commands

### Development

```bash
# Format code
make format
# or
black . && isort .

# Lint code
make lint
# or
python scripts/lint.py

# Run tests
make test
# or
python scripts/test_all.py

# Clean caches
make clean
```

### Project Management

```bash
# Create new project
make new PROJECT=my-new-project
# or
python scripts/create_project.py my-new-project

# Navigate to project
cd projects/my-new-project

# Install project dependencies
pip install -r requirements.txt
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Stage changes
git add .

# Commit (pre-commit hooks run automatically)
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-feature
```

## Project Structure

```
project-name/
├── src/                # Source code
│   ├── __init__.py
│   └── main.py         # Entry point
├── tests/              # Tests
│   ├── __init__.py
│   └── test_main.py
├── data/               # Data files (gitignored)
├── config/             # Configuration files
├── docs/               # Project-specific docs
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── README.md           # Project documentation
```

## Code Patterns

### Basic Setup

```python
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
```

### LLM Call

```python
from openai import OpenAI

client = OpenAI(api_key=API_KEY)

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
```

### Embeddings

```python
from openai import OpenAI

client = OpenAI(api_key=API_KEY)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Text to embed"
)

embedding = response.data[0].embedding
```

### Error Handling

```python
from functools import wraps
import time

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise
                    sleep = (backoff_in_seconds * 2 ** x)
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

@retry_with_backoff(retries=3)
def api_call():
    # Your API call here
    pass
```

## Testing Patterns

```python
import pytest
from unittest.mock import Mock, patch

def test_function():
    """Test description."""
    result = my_function("input")
    assert result == "expected"

@pytest.fixture
def mock_api():
    """Mock external API."""
    with patch('module.api_call') as mock:
        mock.return_value = "mocked"
        yield mock

def test_with_mock(mock_api):
    """Test using mock."""
    result = function_that_calls_api()
    assert mock_api.called
```

## Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000
LOG_LEVEL=INFO
```

## Commit Message Format

```
<type>: <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

## Useful Links

- [Documentation](docs/)
- [Development Guidelines](CONTRIBUTING.md)
- [Architecture Guide](docs/architecture.md)
- [Best Practices](docs/best-practices.md)

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt
```

### API Errors
- Check API keys in `.env`
- Verify API quota/limits
- Check API key permissions

### Test Failures
```bash
# Run specific test
pytest tests/test_file.py::test_function -v

# Run with debugging
pytest --pdb
```

### Pre-commit Issues
```bash
# Update hooks
pre-commit autoupdate

# Run manually
pre-commit run --all-files
```

## Performance Tips

1. **Cache embeddings** - Don't regenerate for same text
2. **Batch API calls** - Process multiple items at once
3. **Use async** - For I/O-bound operations
4. **Monitor costs** - Track token usage
5. **Optimize prompts** - Shorter = faster + cheaper

## Security Checklist

- [ ] API keys in `.env`, not code
- [ ] `.env` in `.gitignore`
- [ ] Input validation implemented
- [ ] Error messages don't leak sensitive data
- [ ] Dependencies up to date
- [ ] Rate limiting in place

---

For more details, see the [Getting Started Guide](docs/getting-started.md).
