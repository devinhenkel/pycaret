"""
State Management Module

Manages application state across workflow steps using Gradio's State component.
Stores data, configuration, models, and results throughout the session.
"""

from typing import Optional, Dict, Any, List, Set
import pandas as pd


class StateManager:
    """
    Manages session state for the PyCaret ML Workflow Manager application.
    
    This class stores and manages all stateful data throughout the workflow:
    - Uploaded dataset
    - Configuration parameters
    - Trained models
    - Evaluation results
    """
    
    def __init__(self):
        """Initialize the state manager with empty state."""
        self.reset()
    
    def reset(self) -> None:
        """Reset all state to initial values."""
        self.data: Optional[pd.DataFrame] = None
        self.data_info: Optional[Dict[str, Any]] = None
        self.problem_type: Optional[str] = None
        self.target_column: Optional[str] = None
        self.setup_config: Optional[Dict[str, Any]] = None
        self.pycaret_setup: Optional[Any] = None  # PyCaret setup object
        self.compare_results: Optional[pd.DataFrame] = None
        self.selected_models: List[str] = []
        self.trained_models: Dict[str, Any] = {}  # model_name -> model_object
        self.current_model: Optional[str] = None
        self.model_metrics: Dict[str, Dict[str, Any]] = {}  # model_name -> metrics
        self.predictions: Optional[pd.DataFrame] = None
        self.plot_choices_cache: Dict[str, List[str]] = {}
        self.invalid_plots: Dict[str, Set[str]] = {}
    
    def set_data(self, data: pd.DataFrame, data_info: Optional[Dict[str, Any]] = None) -> None:
        """Store uploaded dataset and its metadata."""
        self.data = data
        self.data_info = data_info or {}
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """Retrieve stored dataset."""
        return self.data
    
    def set_problem_type(self, problem_type: str) -> None:
        """Store selected problem type."""
        self.problem_type = problem_type
    
    def get_problem_type(self) -> Optional[str]:
        """Retrieve selected problem type."""
        return self.problem_type
    
    def set_target_column(self, target_column: str) -> None:
        """Store selected target column."""
        self.target_column = target_column
    
    def get_target_column(self) -> Optional[str]:
        """Retrieve selected target column."""
        return self.target_column
    
    def set_setup_config(self, config: Dict[str, Any]) -> None:
        """Store setup configuration."""
        self.setup_config = config
    
    def get_setup_config(self) -> Optional[Dict[str, Any]]:
        """Retrieve setup configuration."""
        return self.setup_config
    
    def set_pycaret_setup(self, setup: Any) -> None:
        """Store PyCaret setup object."""
        self.pycaret_setup = setup
    
    def get_pycaret_setup(self) -> Optional[Any]:
        """Retrieve PyCaret setup object."""
        return self.pycaret_setup
    
    def set_compare_results(self, results: pd.DataFrame) -> None:
        """Store model comparison results."""
        self.compare_results = results
    
    def get_compare_results(self) -> Optional[pd.DataFrame]:
        """Retrieve model comparison results."""
        return self.compare_results
    
    def add_trained_model(self, model_name: str, model: Any) -> None:
        """Store a trained model."""
        self.trained_models[model_name] = model
    
    def get_trained_model(self, model_name: str) -> Optional[Any]:
        """Retrieve a trained model by name."""
        return self.trained_models.get(model_name)
    
    def set_current_model(self, model_name: str) -> None:
        """Set the currently selected model for evaluation."""
        self.current_model = model_name
    
    def get_current_model(self) -> Optional[str]:
        """Retrieve the currently selected model."""
        return self.current_model
    
    def set_model_metrics(self, model_name: str, metrics: Dict[str, Any]) -> None:
        """Store metrics for a model."""
        self.model_metrics[model_name] = metrics
    
    def get_model_metrics(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve metrics for a model."""
        return self.model_metrics.get(model_name)
    
    def set_predictions(self, predictions: pd.DataFrame) -> None:
        """Store predictions."""
        self.predictions = predictions
    
    def get_predictions(self) -> Optional[pd.DataFrame]:
        """Retrieve predictions."""
        return self.predictions

    def set_model_plot_choices(self, model_name: str, choices: List[str]) -> None:
        """Cache available plot choices for a specific model."""
        self.plot_choices_cache[model_name] = choices

    def get_model_plot_choices(self, model_name: str) -> List[str]:
        """Retrieve cached plot choices for the model."""
        return self.plot_choices_cache.get(model_name, [])

    def add_invalid_plot(self, model_name: str, plot_type: str) -> None:
        """Mark a plot type as invalid for a given model."""
        invalid_set = self.invalid_plots.setdefault(model_name, set())
        invalid_set.add(plot_type)

    def get_allowed_plots(self, model_name: str, base_choices: List[str]) -> List[str]:
        """Filter out invalid plots from the base list."""
        invalid_set = self.invalid_plots.get(model_name, set())
        return [plot for plot in base_choices if plot not in invalid_set]

