"""
Application Constants

Defines constants used throughout the application.
"""

# Problem Types
PROBLEM_TYPES = [
    'classification',
    'regression',
    'clustering',
    'anomaly_detection',
    'time_series',
]

# Problem Type Labels (for UI)
PROBLEM_TYPE_LABELS = {
    'classification': 'Classification',
    'regression': 'Regression',
    'clustering': 'Clustering',
    'anomaly_detection': 'Anomaly Detection',
    'time_series': 'Time Series Forecasting',
}

# Problem Type Descriptions
PROBLEM_TYPE_DESCRIPTIONS = {
    'classification': 'Predict categorical outcomes (e.g., spam/not spam, disease diagnosis)',
    'regression': 'Predict continuous values (e.g., house prices, temperature)',
    'clustering': 'Group similar data points together (e.g., customer segmentation)',
    'anomaly_detection': 'Identify unusual patterns or outliers in data',
    'time_series': 'Forecast future values based on historical time series data',
}

# Color Scheme
COLORS = {
    'primary': '#2563eb',
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
}

# Workflow Steps
WORKFLOW_STEPS = [
    'Upload Data',
    'Select Problem Type',
    'Configure Setup',
    'Compare Models',
    'Evaluate Models',
    'Export Model',
]

