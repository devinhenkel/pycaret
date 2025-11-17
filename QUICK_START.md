# Quick Start Guide

## Fastest Way to Test

### Option 1: Use the Quick Test Script

```bash
./quick_test.sh
```

This script will:
1. ✅ Check Python installation
2. ✅ Create sample datasets (if needed)
3. ✅ Install dependencies (if needed)
4. ✅ Launch the application

### Option 2: Manual Steps

```bash
# 1. Install dependencies (creates virtual environment automatically)
uv sync

# 2. Create sample datasets (if needed)
uv run python examples/sample_datasets/create_sample_data.py

# 3. Run the application
uv run python main.py
```

**Note**: If you don't have `uv` installed:
```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then follow steps above
```

## What to Test

1. **Upload the sample dataset**:
   - File: `examples/sample_datasets/classification_sample.csv`
   - Should see preview and statistics

2. **Select Problem Type**:
   - Choose "classification"
   - Select "target" as target column

3. **Configure Setup**:
   - Leave defaults or adjust
   - Click "Initialize Setup"

4. **Compare Models**:
   - Click "Compare Models"
   - Wait for results (may take 1-2 minutes)

5. **Evaluate Models**:
   - Select a model from dropdown
   - Try generating plots

6. **Export Model**:
   - Select a model
   - Download model and metadata

## Expected Results

- ✅ Application launches on `http://localhost:7860`
- ✅ File upload works
- ✅ Data preview displays correctly
- ✅ Setup initializes successfully
- ✅ Model comparison completes
- ✅ Models can be evaluated and exported

## Troubleshooting

**If you get import errors:**
```bash
uv sync
```

**If uv is not installed:**
```bash
# Install uv (one-liner)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip (fallback)
pip install uv
```

**If port 7860 is busy:**
- Modify `main.py` to use a different port
- Or stop the process using port 7860

**If PyCaret installation fails:**
```bash
uv add pycaret
# Or manually add to pyproject.toml and run:
uv sync
```

## Need Help?

See `TESTING_GUIDE.md` for detailed testing instructions.

