"""
PyCaret Wrapper Module

Provides a simplified interface to PyCaret operations.
Handles setup initialization, model comparison, and predictions.
"""

from typing import Dict, Any, Optional, List, Tuple
import pandas as pd


class PyCaretWrapper:
    """
    Wrapper for PyCaret operations.
    
    Provides a simplified interface to PyCaret's setup, compare_models,
    and other functions, with error handling and progress tracking.
    """
    
    def __init__(self):
        """Initialize the PyCaret wrapper."""
        self.setup = None
        self.problem_type = None
    
    def initialize_setup(
        self,
        problem_type: str,
        data: pd.DataFrame,
        config: Dict[str, Any]
    ) -> Tuple[Any, Optional[str]]:
        """
        Initialize PyCaret setup based on problem type.
        
        Args:
            problem_type: Type of ML problem (classification, regression, etc.)
            data: DataFrame to use for setup
            config: Setup configuration dictionary
            
        Returns:
            Tuple of (setup_object, error_message)
        """
        try:
            if problem_type == 'classification':
                from pycaret.classification import setup as clf_setup
                self.setup = clf_setup(data=data, **config, silent=True, verbose=False)
            elif problem_type == 'regression':
                from pycaret.regression import setup as reg_setup
                self.setup = reg_setup(data=data, **config, silent=True, verbose=False)
            elif problem_type == 'clustering':
                from pycaret.clustering import setup as clus_setup
                self.setup = clus_setup(data=data, **config, silent=True, verbose=False)
            elif problem_type == 'anomaly_detection':
                from pycaret.anomaly import setup as anom_setup
                self.setup = anom_setup(data=data, **config, silent=True, verbose=False)
            elif problem_type == 'time_series':
                from pycaret.time_series import setup as ts_setup
                self.setup = ts_setup(data=data, **config, silent=True, verbose=False)
            else:
                return None, f"Unsupported problem type: {problem_type}"
            
            self.problem_type = problem_type
            return self.setup, None
            
        except Exception as e:
            return None, f"Error initializing PyCaret setup: {str(e)}"
    
    def compare_models(self, n_select: Optional[int] = None, **kwargs) -> Tuple[pd.DataFrame, Optional[str]]:
        """
        Compare all available models.
        
        Args:
            n_select: Number of top models to return (None for all)
            **kwargs: Additional arguments for compare_models
            
        Returns:
            Tuple of (results_dataframe, error_message)
        """
        if self.setup is None:
            return None, "Setup not initialized. Please initialize setup first."
        
        try:
            if self.problem_type == 'classification':
                from pycaret.classification import compare_models
            elif self.problem_type == 'regression':
                from pycaret.regression import compare_models
            elif self.problem_type == 'clustering':
                from pycaret.clustering import compare_models
            elif self.problem_type == 'anomaly_detection':
                from pycaret.anomaly import compare_models
            elif self.problem_type == 'time_series':
                from pycaret.time_series import compare_models
            else:
                return None, f"Unsupported problem type: {self.problem_type}"
            
            results = compare_models(n_select=n_select, **kwargs)
            return results, None
            
        except Exception as e:
            return None, f"Error comparing models: {str(e)}"
    
    def get_model(self, model_name: str) -> Tuple[Any, Optional[str]]:
        """
        Get a trained model by name.
        
        Args:
            model_name: Name/abbreviation of the model
            
        Returns:
            Tuple of (model_object, error_message)
        """
        if self.setup is None:
            return None, "Setup not initialized."
        
        try:
            if self.problem_type == 'classification':
                from pycaret.classification import create_model
            elif self.problem_type == 'regression':
                from pycaret.regression import create_model
            elif self.problem_type == 'clustering':
                from pycaret.clustering import create_model
            elif self.problem_type == 'anomaly_detection':
                from pycaret.anomaly import create_model
            elif self.problem_type == 'time_series':
                from pycaret.time_series import create_model
            else:
                return None, f"Unsupported problem type: {self.problem_type}"
            
            model = create_model(model_name, verbose=False)
            return model, None
            
        except Exception as e:
            return None, f"Error creating model {model_name}: {str(e)}"
    
    def predict_model(self, model: Any, data: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, Optional[str]]:
        """
        Generate predictions using a trained model.
        
        Args:
            model: Trained model object
            data: Data to predict on (None for test set)
            
        Returns:
            Tuple of (predictions_dataframe, error_message)
        """
        if self.setup is None:
            return None, "Setup not initialized."
        
        try:
            if self.problem_type == 'classification':
                from pycaret.classification import predict_model
            elif self.problem_type == 'regression':
                from pycaret.regression import predict_model
            elif self.problem_type == 'clustering':
                from pycaret.clustering import predict_model
            elif self.problem_type == 'anomaly_detection':
                from pycaret.anomaly import predict_model
            elif self.problem_type == 'time_series':
                from pycaret.time_series import predict_model
            else:
                return None, f"Unsupported problem type: {self.problem_type}"
            
            predictions = predict_model(model, data=data)
            return predictions, None
            
        except Exception as e:
            return None, f"Error generating predictions: {str(e)}"

