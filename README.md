# AI Engineering Projects

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Personal Portfolio & Learning Repository**

A professional monorepo showcasing my AI Engineering skills through production-quality projects. Each project demonstrates practical implementations of modern AI/ML techniques including LLMs, RAG systems, embeddings, and advanced ML engineering practices.

## 🎯 Overview

This repository serves as my personal portfolio of AI engineering work, demonstrating:

- **Production-ready code** with proper error handling and comprehensive testing
- **Scalable architectures** for real-world AI applications
- **Best practices** in ML engineering, LLMOps, and MLOps
- **Well-documented** implementations with detailed explanations
- **Modular design** with reusable, maintainable components
- **Industry-standard** tooling and development workflows

## 📁 Repository Structure

```
ai-engineering-projects/
├── projects/                    # Individual AI projects
│   ├── hallucination-resistant-rag/
│   ├── semantic-search-engine/
│   ├── llm-fine-tuning/
│   └── ... (more projects)
├── docs/                        # Comprehensive documentation
│   ├── getting-started.md
│   ├── architecture.md
│   └── best-practices.md
├── scripts/                     # Automation and utility scripts
│   ├── setup.py
│   ├── test_all.py
│   └── lint.py
├── .editorconfig               # Code style configuration
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── pyproject.toml              # Python project configuration
├── CONTRIBUTING.md             # Development guidelines
└── README.md                   # This file
```

## 🚀 Projects

### 1. Hallucination-Resistant RAG System
**Status:** ✅ Active Development

A sophisticated Retrieval-Augmented Generation system implementing:
- Advanced chunking strategies
- Embedding-based retrieval
- Context-aware generation
- Hallucination detection and mitigation

**Tech Stack:** Python, LangChain, ChromaDB, OpenAI API

[View Project →](projects/hallucination-resistant-rag/)

### 2. Semantic Search Engine
**Status:** 🔜 Planned

Build a high-performance semantic search system with:
- Vector embeddings
- Approximate nearest neighbor search
- Query expansion
- Re-ranking strategies

**Tech Stack:** Python, FAISS, Sentence Transformers

[View Project →](projects/semantic-search-engine/)

### 3. LLM Fine-tuning Pipeline
**Status:** 🔜 Planned

End-to-end pipeline for fine-tuning large language models:
- Data preprocessing
- LoRA/QLoRA implementation
- Evaluation metrics
- Model deployment

**Tech Stack:** Python, PyTorch, Hugging Face Transformers

[View Project →](projects/llm-fine-tuning/)

## 🛠️ Tech Stack

- **Languages:** Python 3.9+
- **ML Frameworks:** PyTorch, TensorFlow, scikit-learn
- **LLM Tools:** LangChain, LlamaIndex, OpenAI API, Anthropic API
- **Vector DBs:** ChromaDB, FAISS, Pinecone, Weaviate
- **Embeddings:** OpenAI Embeddings, Sentence Transformers
- **Development:** pytest, black, ruff, mypy
- **Deployment:** Docker, FastAPI, Streamlit

## 🏁 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip or conda for package management
- Git for version control

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mr-shakib/ai-engineering-projects.git
   cd ai-engineering-projects
   ```

2. **Create a virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda create -n ai-projects python=3.11
   conda activate ai-projects
   ```

3. **Navigate to a project**
   ```bash
   cd projects/hallucination-resistant-rag
   ```

4. **Install project dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

6. **Run the project**
   ```bash
   python src/main.py
   ```

For detailed setup instructions, see the [Getting Started Guide](docs/getting-started.md).

## 📚 Documentation

- [Getting Started](docs/getting-started.md) - Setup and installation
- [Architecture Guide](docs/architecture.md) - System design and patterns
- [Best Practices](docs/best-practices.md) - Code standards and conventions
- [API Reference](docs/api-reference.md) - API documentation

## 🧪 Testing

Each project includes comprehensive tests. To run all tests:

```bash
python scripts/test_all.py
```

To test a specific project:

```bash
cd projects/your-project
pytest tests/
```

## 💼 About This Repository

This is a personal learning and portfolio repository where I explore and implement advanced AI Engineering concepts. While not open for external contributions, I maintain high code quality standards and best practices throughout.

### Development Approach

- Iterative development with clear goals
- Comprehensive documentation and testing
- Production-quality code from the start
- Continuous learning and improvement
- Real-world problem-solving focus

## 📝 Code Quality

This project maintains high code quality standards:

- **Formatting:** [Black](https://github.com/psf/black) with 88 character line length
- **Linting:** [Ruff](https://github.com/astral-sh/ruff) for fast Python linting
- **Type Checking:** [mypy](http://mypy-lang.org/) for static type analysis
- **Testing:** [pytest](https://pytest.org/) with >80% coverage target

Run all checks:
```bash
python scripts/lint.py
```

## 📄 License

This project is available under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Portfolio Repository** | Demonstrating AI Engineering Excellence | Continuously Updated

## 🙏 Acknowledgments

Built with amazing tools and technologies:
- OpenAI for GPT models and embeddings
- Anthropic for Claude models
- The incredible open-source AI/ML community

## 📧 Contact

Interested in my work or want to discuss AI Engineering?
- **LinkedIn**: [Connect with me](https://www.linkedin.com/in/shakib-howlader/)
- **GitHub**: [View my profile](https://github.com/mr-shakib)
- **Email**: contactshakibhere@gmail.com

## 🗺️ Roadmap & Goals

- [ ] Complete Hallucination-Resistant RAG System
- [ ] More to be added

---

**Note:** This is my personal learning and portfolio repository. Projects demonstrate production-quality AI engineering skills and are continuously improved as I learn new techniques.
