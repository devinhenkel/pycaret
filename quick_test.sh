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

# Check and ensure Python 3.11 is available
echo "🐍 Checking Python 3.11 availability..."
if ! uv python list 2>/dev/null | grep -q "3.11"; then
    echo "   Installing Python 3.11 (required for PyCaret)..."
    uv python install 3.11 > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Python 3.11"
        echo "   Please install Python 3.11 manually or check your internet connection"
        exit 1
    fi
    echo "✅ Python 3.11 installed"
else
    echo "✅ Python 3.11 available"
fi
echo ""

# Sync dependencies (creates venv and installs packages)
echo "📦 Syncing dependencies with Python 3.11..."
uv sync --python 3.11 > /dev/null 2>&1

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

