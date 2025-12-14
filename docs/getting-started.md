# Getting Started with AI Engineering Projects

This guide will help you set up your development environment and get started with the AI Engineering Projects monorepo.

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

- **Python 3.9 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** or **conda** - Package managers (pip comes with Python)

### Optional but Recommended

- **VS Code** or **PyCharm** - IDEs with good Python support
- **Docker** - For containerized deployments
- **Make** - For running automated tasks

### API Keys

Many projects require API keys from:

- [OpenAI](https://platform.openai.com/api-keys) - For GPT models and embeddings
- [Anthropic](https://console.anthropic.com/) - For Claude models
- [Cohere](https://dashboard.cohere.ai/api-keys) - For embeddings and reranking
- [Pinecone](https://www.pinecone.io/) - For vector database (optional)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-engineering-projects.git
cd ai-engineering-projects
```

### 2. Set Up Python Environment

Choose one of the following methods:

#### Option A: Using venv (Recommended for beginners)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Option B: Using conda

```bash
# Create conda environment
conda create -n ai-projects python=3.11

# Activate environment
conda activate ai-projects
```

### 3. Verify Installation

```bash
# Check Python version
python --version  # Should be 3.9 or higher

# Check pip
pip --version
```

## Working with Projects

### Navigate to a Project

Each project is self-contained in the `projects/` directory:

```bash
cd projects/hallucination-resistant-rag
```

### Install Project Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Configure Environment Variables

Most projects require API keys and configuration:

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
# On Windows, use: notepad .env
# On macOS/Linux, use: nano .env or vim .env
```

Example `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
COHERE_API_KEY=your-cohere-key

# Optional settings
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000
```

### Run the Project

```bash
# Most projects have a main entry point
python src/main.py

# Or follow project-specific instructions in its README
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

This includes:
- `pytest` - Testing framework
- `black` - Code formatter
- `ruff` - Fast Python linter
- `mypy` - Type checker
- `pre-commit` - Git hooks

### 3. Set Up Pre-commit Hooks

```bash
pre-commit install
```

This automatically runs code quality checks before each commit.

### 4. Make Your Changes

Edit code, add features, fix bugs, etc.

### 5. Run Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_embeddings.py

# Run tests matching a pattern
pytest -k "test_retrieval"
```

### 6. Format and Lint Code

```bash
# Format code with Black
black .

# Sort imports
isort .

# Lint code
ruff check .

# Type check
mypy src/
```

Or run all at once:
```bash
# Format, lint, and test
black . && isort . && ruff check . && pytest
```

### 7. Commit Changes

```bash
git add .
git commit -m "feat: add semantic search capability"
```

### 8. Push and Create PR

```bash
git push origin feature/my-new-feature
```

Then create a Pull Request on GitHub.

## Common Tasks

### Adding a New Dependency

```bash
# Install the package
pip install package-name

# Add to requirements.txt
pip freeze | grep package-name >> requirements.txt

# Or manually edit requirements.txt
```

### Running Jupyter Notebooks

```bash
# Install Jupyter
pip install jupyter

# Start Jupyter
jupyter notebook

# Or use JupyterLab
jupyter lab
```

### Using Docker

```bash
# Build Docker image (if Dockerfile exists)
docker build -t project-name .

# Run container
docker run -p 8000:8000 project-name
```

### Managing Multiple Projects

```bash
# Install all project dependencies
for dir in projects/*/; do
    cd "$dir"
    pip install -r requirements.txt
    cd ../..
done
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:

```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### API Key Errors

If you get API authentication errors:

1. Check `.env` file exists and contains valid keys
2. Ensure keys don't have extra spaces or quotes
3. Verify keys are not expired
4. Check API usage limits

### Python Version Issues

If you need a specific Python version:

```bash
# Using pyenv (macOS/Linux)
pyenv install 3.11.0
pyenv local 3.11.0

# Using conda
conda create -n ai-projects python=3.11
```

### Dependency Conflicts

If you encounter package conflicts:

```bash
# Create fresh environment
deactivate  # If in a virtual environment
rm -rf venv  # Remove old environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Best Practices

### Project Organization

- Keep each project self-contained
- Don't share dependencies between projects
- Use separate virtual environments if needed

### API Keys and Secrets

- Never commit `.env` files
- Use `.env.example` as a template
- Rotate keys regularly
- Use different keys for development/production

### Code Quality

- Write tests for new features
- Document complex logic
- Use type hints
- Follow PEP 8 style guide

### Git Workflow

- Commit early and often
- Write descriptive commit messages
- Keep commits focused and atomic
- Pull before pushing

## Next Steps

1. **Explore Projects** - Browse the `projects/` directory
2. **Read Documentation** - Check project-specific READMEs
3. **Run Examples** - Try running existing projects
4. **Start Building** - Create your own AI projects
5. **Contribute** - See [CONTRIBUTING.md](../CONTRIBUTING.md)

## Additional Resources

### Learning Materials

- [Python Documentation](https://docs.python.org/3/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic Claude Docs](https://docs.anthropic.com/)

### Tools and Libraries

- [Hugging Face](https://huggingface.co/) - Models and datasets
- [Pinecone](https://www.pinecone.io/) - Vector database
- [Weights & Biases](https://wandb.ai/) - Experiment tracking
- [LangSmith](https://www.langchain.com/langsmith) - LLM debugging

### Community

- [GitHub Discussions](https://github.com/yourusername/ai-engineering-projects/discussions)
- [Issues](https://github.com/yourusername/ai-engineering-projects/issues)

## Getting Help

If you run into issues:

1. Check project-specific README
2. Search existing GitHub issues
3. Read error messages carefully
4. Create a new issue with details

Happy coding! 🚀
