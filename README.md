# PyCaret ML Workflow Manager

A comprehensive Gradio-based web application for PyCaret machine learning workflows.

## Overview

This application provides a user-friendly interface for the complete PyCaret ML workflow:
- **Data Upload**: Upload CSV, Excel, or Parquet files
- **Problem Type Selection**: Choose from Classification, Regression, Clustering, Anomaly Detection, or Time Series
- **Setup Configuration**: Configure PyCaret setup parameters
- **Model Comparison**: Compare all available models with one click
- **Model Evaluation**: Evaluate models with detailed metrics and visualizations
- **Model Export**: Download trained models and metadata

## Features

- Support for 5 ML problem types (Classification, Regression, Clustering, Anomaly Detection, Time Series)
- Interactive data preview and statistics
- One-click model comparison
- Comprehensive visualization suite
- Model export with preprocessing pipeline included
- No coding required for standard workflows

## Installation

### Using uv (Recommended)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates virtual environment automatically)
uv sync

# Or install with dev dependencies
uv sync --extra dev
```

### Using pip (Alternative)

```bash
# Install dependencies
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Usage

### Using uv (Recommended)

```bash
# Run the application (automatically uses project environment)
uv run python main.py
```

### Using pip

```bash
# Activate virtual environment first (if using one)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the application
python main.py
```

The application will launch on `http://localhost:7860`

## Project Structure

```
pycaret/
├── main.py                 # Main entry point
├── src/
│   ├── app.py              # Gradio application setup
│   ├── modules/            # Core functionality modules
│   ├── ui/                 # UI components
│   └── utils/              # Utility functions
├── tests/                  # Test files
└── examples/               # Example datasets
```

## Development

See `IMPLEMENTATION_PLAN.md` for detailed implementation plan and architecture.

## Requirements

- Python 3.8+
- PyCaret 3.x
- Gradio 4.x
- See `pyproject.toml` for full dependency list

## License

[Add your license here]
