"""Setup script for the monorepo."""

import subprocess
import sys
from pathlib import Path


def create_venv():
    """Create virtual environment."""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    print("✓ Virtual environment created")


def get_python_executable():
    """Get the path to the Python executable in the venv."""
    if sys.platform == "win32":
        return Path("venv/Scripts/python.exe")
    return Path("venv/bin/python")


def install_dependencies():
    """Install development dependencies."""
    print("\nInstalling development dependencies...")
    python_exe = get_python_executable()

    # Upgrade pip
    subprocess.run(
        [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"], check=True
    )

    # Install common development tools
    dev_packages = [
        "black",
        "ruff",
        "isort",
        "mypy",
        "pytest",
        "pytest-cov",
        "pre-commit",
    ]

    subprocess.run([str(python_exe), "-m", "pip", "install"] + dev_packages, check=True)
    print("✓ Development dependencies installed")


def setup_pre_commit():
    """Set up pre-commit hooks."""
    print("\nSetting up pre-commit hooks...")
    python_exe = get_python_executable()

    subprocess.run([str(python_exe), "-m", "pre_commit", "install"], check=True)
    print("✓ Pre-commit hooks installed")


def create_env_template():
    """Create .env.example template."""
    print("\nCreating .env.example template...")
    env_template = """# API Keys
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
COHERE_API_KEY=your-cohere-key-here

# Model Configuration
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_TOKENS=2000

# Vector Database (optional)
PINECONE_API_KEY=your-pinecone-key-here
PINECONE_ENVIRONMENT=us-east-1-aws
"""

    with open(".env.example", "w") as f:
        f.write(env_template)
    print("✓ .env.example created")


def main():
    """Run setup."""
    print("=" * 60)
    print("AI Engineering Projects - Setup")
    print("=" * 60)

    try:
        create_venv()
        install_dependencies()
        setup_pre_commit()
        create_env_template()

        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Activate virtual environment:")
        if sys.platform == "win32":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("2. Copy .env.example to .env and add your API keys")
        print("3. Navigate to a project: cd projects/project-name")
        print("4. Install project dependencies: pip install -r requirements.txt")
        print("5. Start building! 🚀")

    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error during setup: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
