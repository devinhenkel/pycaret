"""
Configuration Manager Module

Manages PyCaret setup configuration collection and validation.
Handles problem-type-specific configurations.
"""

from typing import Dict, Any, Optional, Tuple


class ConfigManager:
    """
    Manages configuration for PyCaret setup.
    
    Collects and validates setup parameters based on the selected
    problem type and user preferences.
    """
    
    DEFAULT_CONFIG = {
        'session_id': None,
        'train_size': 0.7,
        'fold': 10,
    }
    
    PROBLEM_TYPE_CONFIGS = {
        'classification': {
            'fold': 10,
        },
        'regression': {
            'fold': 10,
        },
        'clustering': {
            'fold': None,  # Not applicable
        },
        'anomaly_detection': {
            'fold': None,
        },
        'time_series': {
            'fold': 5,
        },
    }
    
    def __init__(self):
        """Initialize the configuration manager."""
        pass
    
    def build_setup_config(
        self,
        problem_type: str,
        target_column: Optional[str] = None,
        data: Optional[Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Build PyCaret setup configuration dictionary.
        
        Args:
            problem_type: Type of ML problem
            target_column: Name of target column (if applicable)
            data: DataFrame (if available for inference)
            **kwargs: Additional configuration parameters
            
        Returns:
            Dictionary of setup parameters for PyCaret
        """
        config = self.DEFAULT_CONFIG.copy()
        
        # Add problem-type-specific defaults
        if problem_type in self.PROBLEM_TYPE_CONFIGS:
            config.update(self.PROBLEM_TYPE_CONFIGS[problem_type])
        
        # Add target column if provided
        if target_column:
            config['target'] = target_column
        
        # Override with user-provided parameters
        config.update(kwargs)
        
        # Remove None values (PyCaret will use defaults)
        config = {k: v for k, v in config.items() if v is not None}
        
        return config
    
    def validate_config(self, config: Dict[str, Any], problem_type: str) -> Tuple[bool, Optional[str]]:
        """
        Validate configuration parameters.
        
        Args:
            config: Configuration dictionary to validate
            problem_type: Type of ML problem
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate train_size
        if 'train_size' in config:
            train_size = config['train_size']
            if not 0 < train_size < 1:
                return False, "train_size must be between 0 and 1"
        
        # Validate fold for supervised learning
        if problem_type in ['classification', 'regression', 'time_series']:
            if 'fold' in config and config['fold'] is not None:
                if not isinstance(config['fold'], int) or config['fold'] < 2:
                    return False, "fold must be an integer >= 2"
        
        # Validate target column for supervised learning
        if problem_type in ['classification', 'regression']:
            if 'target' not in config or not config['target']:
                return False, "target column is required for supervised learning"
        
        return True, None
    
    def get_setup_summary(self, config: Dict[str, Any], problem_type: str) -> Dict[str, Any]:
        """
        Generate a human-readable summary of the configuration.
        
        Args:
            config: Configuration dictionary
            problem_type: Type of ML problem
            
        Returns:
            Dictionary with formatted summary
        """
        summary = {
            'problem_type': problem_type,
            'basic_parameters': {},
            'advanced_parameters': {}
        }
        
        basic_params = ['target', 'session_id', 'train_size', 'fold']
        for param in basic_params:
            if param in config:
                summary['basic_parameters'][param] = config[param]
        
        # All other parameters are advanced
        for key, value in config.items():
            if key not in basic_params:
                summary['advanced_parameters'][key] = value
        
        return summary

