"""
Model Manager Module

Handles model storage, export, and metadata generation.
Manages model serialization and download functionality.
"""

from typing import Dict, Any, Optional, Tuple
import json
from datetime import datetime
import os


class ModelManager:
    """
    Manages model export and metadata generation.
    
    Handles saving models as pickle files, generating metadata JSON,
    and creating downloadable file objects.
    """
    
    def __init__(self):
        """Initialize the model manager."""
        pass
    
    def save_model(
        self,
        model: Any,
        problem_type: str,
        model_name: str,
        output_dir: str = "models"
    ) -> Tuple[str, Optional[str]]:
        """
        Save a trained model using PyCaret's save_model function.
        This ensures the preprocessing pipeline is included.
        
        Args:
            model: Trained model object to save
            problem_type: Type of ML problem
            model_name: Name/abbreviation of the model
            output_dir: Directory to save the model
            
        Returns:
            Tuple of (absolute_file_path, error_message)
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename (without .pkl extension - PyCaret will add it)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_base = f"{problem_type}_{model_name}_{timestamp}"
            file_path_base = os.path.join(output_dir, filename_base)
            
            # Use PyCaret's save_model to include preprocessing pipeline
            # Import the appropriate save_model function
            if problem_type == 'classification':
                from pycaret.classification import save_model as pycaret_save_model
            elif problem_type == 'regression':
                from pycaret.regression import save_model as pycaret_save_model
            elif problem_type == 'clustering':
                from pycaret.clustering import save_model as pycaret_save_model
            elif problem_type == 'anomaly_detection':
                from pycaret.anomaly import save_model as pycaret_save_model
            elif problem_type == 'time_series':
                from pycaret.time_series import save_model as pycaret_save_model
            else:
                return None, f"Unsupported problem type: {problem_type}"
            
            # Save using PyCaret (includes preprocessing pipeline)
            # PyCaret automatically adds .pkl extension
            pycaret_save_model(model, file_path_base, verbose=False)
            
            # PyCaret saves with .pkl extension
            file_path = file_path_base + '.pkl'
            abs_path = os.path.abspath(file_path)
            
            # Verify file was created
            if not os.path.exists(abs_path):
                # Check if file exists without .pkl (shouldn't happen, but just in case)
                if os.path.exists(file_path_base):
                    abs_path = os.path.abspath(file_path_base)
                else:
                    return None, f"Model file was not created. Expected: {abs_path}"
            
            return abs_path, None
            
        except Exception as e:
            import traceback
            return None, f"Error saving model: {str(e)}\n{traceback.format_exc()}"
    
    def generate_metadata(
        self,
        model_name: str,
        problem_type: str,
        setup_config: Dict[str, Any],
        metrics: Dict[str, Any],
        hyperparameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate model metadata dictionary.
        
        Args:
            model_name: Name of the model
            problem_type: Type of ML problem
            setup_config: Setup configuration used
            metrics: Model performance metrics
            hyperparameters: Model hyperparameters (optional)
            
        Returns:
            Dictionary containing model metadata
        """
        metadata = {
            'model_name': model_name,
            'problem_type': problem_type,
            'date_created': datetime.now().isoformat(),
            'setup_configuration': setup_config,
            'performance_metrics': metrics,
            'hyperparameters': hyperparameters or {},
        }
        
        return metadata
    
    def save_metadata(
        self,
        metadata: Dict[str, Any],
        output_dir: str = "models"
    ) -> Tuple[str, Optional[str]]:
        """
        Save model metadata as a JSON file.
        
        Args:
            metadata: Metadata dictionary to save
            output_dir: Directory to save the metadata
            
        Returns:
            Tuple of (file_path, error_message)
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename
            model_name = metadata.get('model_name', 'model')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{model_name}_metadata_{timestamp}.json"
            file_path = os.path.join(output_dir, filename)
            
            # Save metadata
            with open(file_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            # Convert to absolute path for Gradio
            abs_path = os.path.abspath(file_path)
            
            # Verify file was created
            if not os.path.exists(abs_path):
                return None, "Metadata file was not created"
            
            return abs_path, None
            
        except Exception as e:
            return None, f"Error saving metadata: {str(e)}"

