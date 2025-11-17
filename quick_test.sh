#!/bin/bash
# Quick test script for PyCaret ML Workflow Manager

echo "🚀 PyCaret ML Workflow Manager - Quick Test"
echo "============================================"
echo ""

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    
    if ! command -v uv &> /dev/null; then
        echo "❌ Failed to install uv. Please install manually:"
        echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo "   Or: pip install uv"
        exit 1
    fi
    echo "✅ uv installed"
    echo ""
fi

echo "✅ uv found: $(uv --version)"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 12 ]; then
    echo "⚠️  Warning: Python $PYTHON_VERSION detected"
    echo "   PyCaret requires Python 3.9, 3.10, or 3.11"
    echo "   uv will automatically use a compatible Python version"
    echo ""
fi

# Sync dependencies (creates venv and installs packages)
echo "📦 Syncing dependencies..."
# Use Python 3.11 if available, otherwise let uv choose compatible version
if uv python list 2>/dev/null | grep -q "3.11"; then
    echo "   Using Python 3.11 (PyCaret compatible)"
    uv sync --python 3.11 > /dev/null 2>&1
else
    echo "   Installing Python 3.11..."
    uv python install 3.11 > /dev/null 2>&1
    uv sync --python 3.11 > /dev/null 2>&1
fi

if [ $? -eq 0 ]; then
    echo "✅ Dependencies synced"
else
    echo "⚠️  Dependency sync had issues, but continuing..."
fi
echo ""

# Create sample datasets if they don't exist
if [ ! -f "examples/sample_datasets/classification_sample.csv" ]; then
    echo "📊 Creating sample datasets..."
    uv run --python 3.11 python examples/sample_datasets/create_sample_data.py
    echo ""
fi

# Check if dependencies are installed
echo "📦 Verifying dependencies..."
if ! uv run --python 3.11 python -c "import gradio, pycaret" 2>/dev/null; then
    echo "⚠️  Dependencies not found. Re-syncing..."
    uv sync --python 3.11
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies verified"
fi
echo ""

# Start the application
echo "🌐 Starting application..."
echo "   The app will open in your browser at http://localhost:7860"
echo "   Press Ctrl+C to stop the server"
echo ""
echo "📝 Test dataset available at:"
echo "   examples/sample_datasets/classification_sample.csv"
echo ""

uv run --python 3.11 python main.py

