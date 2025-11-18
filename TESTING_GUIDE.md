# Testing Guide

## Quick Start

### 1. Install Dependencies

```bash
# Make sure you're in the project directory
cd /media/devinhenkel/Factory/Projects/pycaret

# Install the package and dependencies using uv
uv sync

# Or if you need dev dependencies:
uv sync --extra dev
```

**Note**: 
- **Python 3.11 is required** (PyCaret only supports Python 3.9, 3.10, and 3.11)
- If you don't have `uv` installed, install it first: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- `uv` will automatically install Python 3.11 if needed: `uv python install 3.11`
- PyCaret installation can take several minutes as it installs many ML libraries.
- `uv sync --python 3.11` will create a virtual environment with Python 3.11 and install all dependencies.

### 2. Create a Test Dataset

We've created sample datasets in `examples/sample_datasets/`:
- `classification_sample.csv` - For testing classification
- `regression_sample.csv` - For testing regression

Or use your own CSV file with:
- At least 10 rows
- At least 2 columns
- For classification: one categorical target column
- For regression: one numeric target column

### 3. Run the Application

```bash
# Using uv with Python 3.11 (required)
uv run --python 3.11 python main.py

# Or activate the environment and run directly
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

The application will:
- Start a Gradio server
- Display a URL (usually `http://127.0.0.1:7860`)
- Open in your default browser automatically

### 4. Test the Workflow

Follow these steps in the web interface:

## Step-by-Step Testing

### Step 1: Upload Data ✅

1. **Go to "Step 1: Upload Data" tab**
2. **Click "Upload Dataset"** or drag and drop a CSV file
3. **Verify**:
   - ✅ Status message shows "File loaded successfully!"
   - ✅ Data Preview shows first 10 rows
   - ✅ Dataset Statistics shows dimensions, data types, missing values

**Test Files**:
- Use `examples/sample_datasets/classification_sample.csv`
- Or any CSV with at least 10 rows

**Expected Results**:
- File uploads without errors
- Preview table displays correctly
- Statistics JSON shows proper structure

---

### Step 2: Select Problem Type ✅

1. **Go to "Step 2: Select Problem Type" tab**
2. **Select a problem type** (e.g., "classification")
3. **Verify**:
   - ✅ Problem description appears
   - ✅ Target column dropdown populates with column names
   - ✅ If classification/regression: suggested target column appears

**Test Cases**:
- Try each problem type (classification, regression, clustering, etc.)
- Verify target column dropdown updates correctly
- Check that auto-detection suggests appropriate columns

**Expected Results**:
- Description text appears for selected problem type
- Target column dropdown shows all columns
- Suggested target column highlighted (if applicable)

---

### Step 3: Configure Setup ✅

1. **Go to "Step 3: Configure Setup" tab**
2. **Select target column** (if required for your problem type)
3. **Adjust parameters** (optional):
   - Session ID (leave empty for auto-generated)
   - Train/Test Split Ratio (default 0.7)
   - Cross-Validation Folds (default 10)
4. **Verify**:
   - ✅ Setup Summary updates automatically
   - ✅ Status shows "Configuration ready"
5. **Click "Initialize Setup"**
6. **Verify**:
   - ✅ Status shows "PyCaret setup initialized successfully!"

**Test Cases**:
- Try different train/test split ratios
- Try different CV fold values
- Test with and without session ID
- Test initialization with valid configuration

**Expected Results**:
- Setup summary JSON displays configuration
- Setup initialization succeeds
- Status message confirms success

---

### Step 4: Compare Models ⚠️

1. **Go to "Step 4: Compare Models" tab**
2. **Click "Compare Models" button**
3. **Wait** (this can take 1-5 minutes depending on dataset size)
4. **Verify**:
   - ✅ Progress message appears
   - ✅ Results table displays model comparison
   - ✅ Model selection checkboxes populate

**Test Cases**:
- Test with small dataset first (< 100 rows)
- Verify results table shows model names and metrics
- Check that model selection updates

**Expected Results**:
- Model comparison completes successfully
- Results table shows multiple models with metrics
- Checkboxes allow selecting models

**Known Issues**:
- May take time for large datasets
- Progress indicator may not show detailed progress yet

---

### Step 5: Evaluate Models ⚠️

1. **Go to "Step 5: Evaluate Models" tab**
2. **Select models** in Step 4 checkboxes
3. **Select a model** from the dropdown
4. **Verify**:
   - ✅ Model metrics display (may be placeholder initially)
   - ✅ Plot type dropdown populates
5. **Select a plot type**
6. **Verify**:
   - ✅ Plot displays (if PyCaret integration works)

**Test Cases**:
- Select different models
- Try different plot types
- Verify metrics display

**Expected Results**:
- Model loads successfully
- Plot types available for problem type
- Plots generate and display

**Known Issues**:
- Metrics may show placeholder data initially
- Some plot types may need additional configuration

---

### Step 6: Export Model ✅

1. **Go to "Step 6: Export Model" tab**
2. **Select a model** from dropdown
3. **Verify**:
   - ✅ Model summary displays
   - ✅ Status shows "ready for export"
4. **Click "Download Model (.pkl)"**
5. **Click "Download Metadata (.json)"**
6. **Verify**:
   - ✅ Files download successfully
   - ✅ Model file is a valid pickle file
   - ✅ Metadata file is valid JSON

**Test Cases**:
- Export different models
- Verify downloaded files
- Check metadata structure

**Expected Results**:
- Model downloads as .pkl file
- Metadata downloads as .json file
- Files are saved to `models/` directory

---

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# If you get import errors, make sure dependencies are installed:
uv sync

# Or if using uv run:
uv run python -c "import gradio"
```

#### 2. PyCaret Not Found
```bash
# PyCaret should be installed via uv sync, but if needed:
uv add pycaret
```

#### 3. Port Already in Use
```bash
# If port 7860 is busy, modify main.py to use a different port:
app.launch(server_port=7861)
```

#### 4. File Upload Fails
- Check file format (CSV, Excel, or Parquet)
- Ensure file has at least 10 rows
- Check file size (max 500MB)

#### 5. Setup Initialization Fails
- Verify target column is selected (for supervised learning)
- Check that data has valid format
- Ensure no critical missing values

#### 6. Model Comparison Takes Too Long
- Use smaller dataset for testing (< 1000 rows)
- Reduce number of CV folds
- Check system resources

---

## Testing Checklist

### Basic Functionality
- [ ] Application launches without errors
- [ ] All 6 tabs are accessible
- [ ] File upload works
- [ ] Data preview displays
- [ ] Statistics calculate correctly

### Workflow Steps
- [ ] Step 1: Upload works
- [ ] Step 2: Problem type selection works
- [ ] Step 3: Setup configuration works
- [ ] Step 4: Model comparison works
- [ ] Step 5: Model evaluation works
- [ ] Step 6: Model export works

### Error Handling
- [ ] Invalid file format shows error
- [ ] Missing required fields show errors
- [ ] Invalid configuration shows errors
- [ ] Error messages are user-friendly

### Edge Cases
- [ ] Small datasets (< 20 rows)
- [ ] Large datasets (> 1000 rows)
- [ ] Datasets with missing values
- [ ] Datasets with many columns
- [ ] Different file formats (CSV, Excel, Parquet)

---

## Sample Test Dataset

A sample classification dataset has been created at:
`examples/sample_datasets/classification_sample.csv`

This dataset contains:
- 100 rows
- 5 feature columns
- 1 target column (categorical)
- No missing values
- Suitable for quick testing

---

## Next Steps After Testing

1. **Report Issues**: Note any bugs or unexpected behavior
2. **Performance Testing**: Test with larger datasets
3. **Feature Requests**: Suggest improvements
4. **Documentation**: Update docs based on findings

---

## Quick Test Command

```bash
# One-liner to install and run with uv (Python 3.11):
uv sync --python 3.11 && uv run --python 3.11 python main.py

# Or if uv is not in PATH:
curl -LsSf https://astral.sh/uv/install.sh | sh && uv sync --python 3.11 && uv run --python 3.11 python main.py
```

Then open `http://localhost:7860` in your browser and start testing!

