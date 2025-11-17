"""
Visualization Module

Handles plot generation using PyCaret's plot_model function.
Supports multiple plot types based on problem type.
"""

from typing import Dict, Any, Optional, List, Tuple
import pandas as pd


class VisualizationManager:
    """
    Manages visualization generation for PyCaret models.
    
    Provides methods to generate various plots based on problem type
    and handles plot type selection and formatting.
    """
    
    CLASSIFICATION_PLOTS = [
        'confusion_matrix',
        'auc',
        'pr',
        'error',
        'class_report',
        'boundary',
        'learning',
        'feature',
    ]
    
    REGRESSION_PLOTS = [
        'residuals',
        'error',
        'learning',
        'feature',
        'manifold',
    ]
    
    CLUSTERING_PLOTS = [
        'elbow',
        'silhouette',
        'distance',
        'distribution',
    ]
    
    TIMESERIES_PLOTS = [
        'forecast',
        'diagnostics',
        'insample',
        'residuals',
    ]
    
    ANOMALY_PLOTS = [
        'tsne',
        'umap',
    ]
    
    def __init__(self):
        """Initialize the visualization manager."""
        self.problem_type = None
        self.setup = None
    
    def set_problem_type(self, problem_type: str) -> None:
        """Set the problem type for plot generation."""
        self.problem_type = problem_type
    
    def set_setup(self, setup: Any) -> None:
        """Set the PyCaret setup object."""
        self.setup = setup
    
    def get_available_plots(self, problem_type: Optional[str] = None) -> List[str]:
        """
        Get list of available plots for a problem type.
        
        Args:
            problem_type: Type of ML problem (uses self.problem_type if None)
            
        Returns:
            List of available plot types
        """
        pt = problem_type or self.problem_type
        if pt == 'classification':
            return self.CLASSIFICATION_PLOTS
        elif pt == 'regression':
            return self.REGRESSION_PLOTS
        elif pt == 'clustering':
            return self.CLUSTERING_PLOTS
        elif pt == 'time_series':
            return self.TIMESERIES_PLOTS
        elif pt == 'anomaly_detection':
            return self.ANOMALY_PLOTS
        else:
            return []
    
    def generate_plot(
        self,
        model: Any,
        plot_type: str,
        problem_type: Optional[str] = None,
        **kwargs
    ) -> Tuple[Any, Optional[str]]:
        """
        Generate a plot for a trained model.
        
        Args:
            model: Trained model object
            plot_type: Type of plot to generate
            problem_type: Type of ML problem (uses self.problem_type if None)
            **kwargs: Additional arguments for plot_model
            
        Returns:
            Tuple of (plot_object, error_message)
        """
        if self.setup is None:
            return None, "Setup not initialized."
        
        pt = problem_type or self.problem_type
        if pt is None:
            return None, "Problem type not set."
        
        try:
            if pt == 'classification':
                from pycaret.classification import plot_model
            elif pt == 'regression':
                from pycaret.regression import plot_model
            elif pt == 'clustering':
                from pycaret.clustering import plot_model
            elif pt == 'anomaly_detection':
                from pycaret.anomaly import plot_model
            elif pt == 'time_series':
                from pycaret.time_series import plot_model
            else:
                return None, f"Unsupported problem type: {pt}"
            
            # Use plotly backend for interactive plots
            plot_kwargs = {'plot': plot_type, 'display_format': 'plotly', **kwargs}
            plot = plot_model(model, **plot_kwargs)
            return plot, None
            
        except Exception as e:
            return None, f"Error generating plot {plot_type}: {str(e)}"

