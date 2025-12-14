# Projects Directory

This directory contains all individual AI Engineering projects in the monorepo.

## Structure

Each project is self-contained with its own:
- Source code (`src/`)
- Tests (`tests/`)
- Documentation (`README.md`)
- Dependencies (`requirements.txt`)
- Configuration (`.env.example`)

## Creating a New Project

Use the project creation script:

```bash
python scripts/create_project.py your-project-name
```

This will generate a complete project structure with all necessary files.

## Existing Projects

### hallucination-resistant-rag
A sophisticated RAG system with hallucination detection and mitigation.

**Status:** Active Development  
**Tech:** Python, LangChain, ChromaDB, OpenAI

[View Project →](hallucination-resistant-rag/)

---

## Project Guidelines

1. **Self-contained** - Each project should be independently runnable
2. **Well-documented** - Include comprehensive README
3. **Tested** - Maintain >80% test coverage
4. **Configurable** - Use .env for configuration
5. **Professional** - Production-quality code

## Shared Resources

While projects are independent, they can share:
- Documentation patterns (from `/docs/`)
- Code quality standards (from root config files)
- Best practices and architectural patterns

## Development Notes

Personal development workflow:
1. Define project goals and architecture
2. Implement with production-quality standards
3. Document thoroughly for future reference
4. Test comprehensively
5. Iterate and improve

## Questions or Issues?

See the [Getting Started Guide](../docs/getting-started.md) for setup and development information.
