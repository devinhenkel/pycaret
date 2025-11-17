"""
Data Handler Module

Handles file upload, validation, preview, and basic data operations.
Supports CSV, Excel (.xlsx, .xls), and Parquet file formats.
"""

from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np


class DataHandler:
    """
    Handles data upload, validation, and preview operations.
    
    Supports multiple file formats and provides data validation,
    preview generation, and statistics calculation.
    """
    
    SUPPORTED_FORMATS = ['.csv', '.xlsx', '.xls', '.parquet']
    MAX_FILE_SIZE_MB = 500
    MIN_ROWS = 10
    HIGH_MISSING_THRESHOLD = 0.30  # 30%
    
    def __init__(self):
        """Initialize the data handler."""
        pass
    
    def load_file(self, file_path: str) -> Tuple[pd.DataFrame, Optional[str]]:
        """
        Load a file into a pandas DataFrame.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            Tuple of (DataFrame, error_message)
            If successful, error_message is None
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.parquet'):
                df = pd.read_parquet(file_path)
            else:
                return None, f"Unsupported file format. Supported: {', '.join(self.SUPPORTED_FORMATS)}"
            
            return df, None
        except Exception as e:
            return None, f"Error loading file: {str(e)}"
    
    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """
        Validate the uploaded dataset.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if df is None or df.empty:
            return False, "Dataset is empty"
        
        if len(df) < self.MIN_ROWS:
            return False, f"Dataset must have at least {self.MIN_ROWS} rows"
        
        if len(df.columns) == 0:
            return False, "Dataset must have at least one column"
        
        # Check for high missing values
        missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if missing_pct > self.HIGH_MISSING_THRESHOLD:
            return True, f"Warning: {missing_pct*100:.1f}% of values are missing"
        
        return True, None
    
    def get_data_preview(self, df: pd.DataFrame, n_rows: int = 10) -> Dict[str, Any]:
        """
        Generate data preview (first and last N rows).
        
        Args:
            df: DataFrame to preview
            n_rows: Number of rows to show from start and end
            
        Returns:
            Dictionary with 'first_rows' and 'last_rows' DataFrames
        """
        first_rows = df.head(n_rows)
        last_rows = df.tail(n_rows)
        
        return {
            'first_rows': first_rows,
            'last_rows': last_rows,
            'total_rows': len(df),
            'total_columns': len(df.columns)
        }
    
    def get_data_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate basic statistics for the dataset.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with statistics including:
            - dimensions
            - data types
            - numeric statistics
            - missing values
        """
        stats = {
            'dimensions': {
                'rows': len(df),
                'columns': len(df.columns)
            },
            'data_types': df.dtypes.astype(str).to_dict(),
            'numeric_stats': {},
            'missing_values': {}
        }
        
        # Numeric statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats['numeric_stats'] = df[numeric_cols].describe().to_dict()
        
        # Missing values
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        stats['missing_values'] = {
            col: {
                'count': int(missing[col]),
                'percentage': float(missing_pct[col])
            }
            for col in df.columns
        }
        
        return stats
    
    def detect_target_column(self, df: pd.DataFrame, problem_type: str) -> Optional[str]:
        """
        Auto-detect likely target column based on column names and data types.
        
        Args:
            df: DataFrame to analyze
            problem_type: Type of ML problem (classification, regression, etc.)
            
        Returns:
            Name of detected target column, or None if not found
        """
        target_keywords = ['target', 'label', 'class', 'outcome', 'y', 'dependent']
        
        # Check for exact matches or contains
        for col in df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in target_keywords):
                return col
        
        # For classification, prefer categorical columns
        if problem_type == 'classification':
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(categorical_cols) > 0:
                return categorical_cols[0]
        
        # For regression, prefer numeric columns
        if problem_type == 'regression':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                return numeric_cols[-1]  # Often the last column
        
        return None

