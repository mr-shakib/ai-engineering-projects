"""Create a new project from template."""

import sys
from pathlib import Path


def create_project_structure(project_name: str):
    """Create a new project with standard structure."""
    project_dir = Path("projects") / project_name

    if project_dir.exists():
        print(f"Error: Project '{project_name}' already exists.")
        sys.exit(1)

    print(f"Creating project: {project_name}")

    # Create directory structure
    directories = [
        project_dir,
        project_dir / "src",
        project_dir / "tests",
        project_dir / "data",
        project_dir / "config",
        project_dir / "docs",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")

    # Create __init__.py files
    (project_dir / "src" / "__init__.py").touch()
    (project_dir / "tests" / "__init__.py").touch()

    # Create .gitkeep for empty directories
    (project_dir / "data" / ".gitkeep").touch()

    # Create README.md
    readme_content = f"""# {project_name.replace('-', ' ').title()}

Brief description of the project.

## Overview

Explain what this project does and why it exists.

## Features

- Feature 1
- Feature 2
- Feature 3

## Architecture

High-level description of the system design.

## Installation

```bash
# Navigate to project directory
cd projects/{project_name}

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Usage

```python
# Example usage
from src.main import main

main()
```

## Configuration

Describe configuration options in config/ or .env

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## API Reference

Document main functions and classes.

## Development

See [Development Guidelines](../../CONTRIBUTING.md) for my personal workflow and standards.

## License

MIT License - see [LICENSE](../../LICENSE)
"""

    with open(project_dir / "README.md", "w") as f:
        f.write(readme_content)
    print("✓ Created README.md")

    # Create requirements.txt
    requirements_content = """# Core dependencies
python-dotenv>=1.0.0

# Add project-specific dependencies here
# Example:
# openai>=1.0.0
# langchain>=0.1.0
# chromadb>=0.4.0
"""

    with open(project_dir / "requirements.txt", "w") as f:
        f.write(requirements_content)
    print("✓ Created requirements.txt")

    # Create .env.example
    env_example_content = """# API Keys
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here

# Model Configuration
MODEL_NAME=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000
"""

    with open(project_dir / ".env.example", "w") as f:
        f.write(env_example_content)
    print("✓ Created .env.example")

    # Create main.py
    main_py_content = '''"""Main entry point for the project."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main function."""
    logger.info("Starting application...")
    
    # Your code here
    
    logger.info("Application finished.")


if __name__ == "__main__":
    main()
'''

    with open(project_dir / "src" / "main.py", "w") as f:
        f.write(main_py_content)
    print("✓ Created src/main.py")

    # Create test file
    test_content = '''"""Tests for main module."""

import pytest
from src.main import main


def test_main():
    """Test main function."""
    # Add your tests here
    pass
'''

    with open(project_dir / "tests" / "test_main.py", "w") as f:
        f.write(test_content)
    print("✓ Created tests/test_main.py")

    print(f"\n✓ Project '{project_name}' created successfully!")
    print("\nNext steps:")
    print(f"1. cd projects/{project_name}")
    print("2. Update requirements.txt with your dependencies")
    print("3. Copy .env.example to .env and add your API keys")
    print("4. pip install -r requirements.txt")
    print("5. Start coding in src/")


def main():
    """Create a new project."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_project.py <project-name>")
        sys.exit(1)

    project_name = sys.argv[1]

    # Validate project name
    if not project_name.replace("-", "").replace("_", "").isalnum():
        print(
            "Error: Project name should only contain letters, numbers, hyphens, and underscores."
        )
        sys.exit(1)

    create_project_structure(project_name)


if __name__ == "__main__":
    main()
