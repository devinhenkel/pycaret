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

# Sync dependencies (creates venv and installs packages)
echo "📦 Syncing dependencies..."
uv sync > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Dependencies synced"
else
    echo "⚠️  Dependency sync had issues, but continuing..."
fi
echo ""

# Create sample datasets if they don't exist
if [ ! -f "examples/sample_datasets/classification_sample.csv" ]; then
    echo "📊 Creating sample datasets..."
    uv run python examples/sample_datasets/create_sample_data.py
    echo ""
fi

# Check if dependencies are installed
echo "📦 Verifying dependencies..."
if ! uv run python -c "import gradio" 2>/dev/null; then
    echo "⚠️  Gradio not found. Re-syncing dependencies..."
    uv sync
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

uv run python main.py

