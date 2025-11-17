"""
Model Manager Module

Handles model storage, export, and metadata generation.
Manages model serialization and download functionality.
"""

from typing import Dict, Any, Optional, Tuple
import pickle
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
        Save a trained model as a pickle file.
        
        Args:
            model: Trained model object to save
            problem_type: Type of ML problem
            model_name: Name/abbreviation of the model
            output_dir: Directory to save the model
            
        Returns:
            Tuple of (file_path, error_message)
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{problem_type}_{model_name}_{timestamp}.pkl"
            file_path = os.path.join(output_dir, filename)
            
            # Save model
            with open(file_path, 'wb') as f:
                pickle.dump(model, f)
            
            return file_path, None
            
        except Exception as e:
            return None, f"Error saving model: {str(e)}"
    
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
            
            return file_path, None
            
        except Exception as e:
            return None, f"Error saving metadata: {str(e)}"

