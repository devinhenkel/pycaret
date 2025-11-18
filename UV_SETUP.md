# Using uv as Package Manager

This project uses `uv` as the recommended package manager. `uv` is a fast Python package installer and resolver written in Rust.

**Important**: This project requires **Python 3.11** (PyCaret requirement). `uv` will automatically manage Python 3.11 for you.

## Why uv?

- ⚡ **Fast**: 10-100x faster than pip
- 🔒 **Reliable**: Better dependency resolution
- 📦 **Modern**: Built-in virtual environment management
- 🎯 **Simple**: One command to sync everything

## Installation

### Install uv

```bash
# One-liner installation
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip (fallback)
pip install uv

# Or using homebrew (macOS)
brew install uv
```

After installation, restart your terminal or run:
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

## Basic Usage

### Sync Dependencies

```bash
# Install all dependencies with Python 3.11 (creates .venv automatically)
uv sync --python 3.11

# Install with dev dependencies
uv sync --python 3.11 --extra dev
```

### Run Commands

```bash
# Run Python scripts in project environment (Python 3.11)
uv run --python 3.11 python main.py

# Run any command in project environment
uv run --python 3.11 pytest
uv run --python 3.11 python -m black .
```

### Add Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Add with version constraint
uv add "package-name>=1.0.0"
```

### Remove Dependencies

```bash
# Remove a dependency
uv remove package-name
```

## Workflow

### Initial Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd pycaret

# 2. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Sync dependencies with Python 3.11
uv sync --python 3.11

# 4. Run the application
uv run --python 3.11 python main.py
```

### Daily Development

```bash
# Run the app (Python 3.11)
uv run --python 3.11 python main.py

# Run tests
uv run --python 3.11 pytest

# Format code
uv run --python 3.11 black .

# Lint code
uv run --python 3.11 ruff check .
```

## Virtual Environment

`uv` automatically creates and manages a `.venv` directory. You don't need to manually create or activate it when using `uv run`.

If you prefer to manually activate:

```bash
# Activate (uv creates .venv automatically)
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Then use regular Python commands
python main.py
```

## Lock File

`uv` creates a `uv.lock` file that locks all dependency versions. This ensures reproducible builds across different machines.

**Important**: Commit `uv.lock` to version control for reproducible builds.

## Migration from pip

If you're migrating from pip:

1. **Remove old virtual environment** (optional):
   ```bash
   rm -rf .venv venv
   ```

2. **Sync with uv**:
   ```bash
   uv sync --python 3.11
   ```

3. **Update your workflow**:
   - Replace `pip install -e .` with `uv sync --python 3.11`
   - Replace `python script.py` with `uv run --python 3.11 python script.py`

## Troubleshooting

### uv not found

```bash
# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Or reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Dependency conflicts

```bash
# Clear cache and re-sync with Python 3.11
rm -rf .venv uv.lock
uv sync --python 3.11
```

### Slow sync

```bash
# Use faster index (if available)
uv sync --index-url https://pypi.org/simple
```

## More Information

- [uv Documentation](https://github.com/astral-sh/uv)
- [uv GitHub](https://github.com/astral-sh/uv)

