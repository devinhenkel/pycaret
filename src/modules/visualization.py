
"""
Visualization Module

Handles plot generation using PyCaret's plot_model function.
Supports multiple plot types based on problem type.
"""

from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments
import matplotlib.pyplot as plt


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
            
            # Generate plot - PyCaret creates matplotlib figures but returns None
            # We need to capture the figure after plot_model is called
            # Force matplotlib backend by setting display_format='text' or system='False'
            plot_kwargs = {
                'plot': plot_type, 
                'save': False,
                'system': False,  # Prevents automatic display
                **kwargs
            }
            
            # Store current figure count before generating plot
            initial_fig_count = len(plt.get_fignums())
            
            # Call plot_model - it creates a figure and may return it or None
            # We'll try to capture the return value first, then fall back to plt.gcf()
            result = plot_model(model, **plot_kwargs)
            
            # Check if plot_model returned a figure object
            if result is not None and hasattr(result, 'savefig'):
                # plot_model returned a matplotlib figure
                fig = result
            elif result is not None and hasattr(result, 'write_html'):
                # plot_model returned a Plotly figure - Gradio can handle this too
                return result, None
            else:
                # plot_model returned None or something else, get the current matplotlib figure
                fig = plt.gcf()
            
            # Verify we got a figure
            if fig is None or not hasattr(fig, 'savefig'):
                # Try to get the most recent figure
                fig_nums = plt.get_fignums()
                if fig_nums:
                    fig = plt.figure(fig_nums[-1])
                else:
                    print(f"❌ No matplotlib figure found for plot type '{plot_type}'")
                    return None, f"Failed to generate plot. PyCaret may not have created a figure for plot type '{plot_type}'."
            
            # Ensure figure has content and is properly formatted
            axes = fig.get_axes()
            if len(axes) == 0:
                print(f"❌ Figure has no axes for plot type '{plot_type}'")
                return None, f"Plot figure is empty. Plot type '{plot_type}' may not be supported for this model."
            
            print(f"✅ Generated matplotlib figure with {len(axes)} axes for plot type '{plot_type}'")
            
            # Apply tight layout to prevent clipping
            try:
                fig.tight_layout(pad=1.0)
            except Exception as e:
                # Some plots may not support tight_layout, try adjust_subplots instead
                try:
                    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
                except Exception:
                    pass  # If both fail, continue anyway
            
            # Ensure figure is properly rendered
            try:
                # Force a draw to ensure the figure is fully rendered
                fig.canvas.draw()
            except Exception as e:
                # Some backends may not support draw()
                print(f"⚠️ Could not draw canvas: {e}")
                pass
            
            # CRITICAL: Return the matplotlib figure object directly
            # DO NOT call fig.show() - this won't work in Gradio
            # DO NOT return None - return the figure object
            # Gradio's gr.Plot() component will handle rendering the figure
            print(f"✅ Returning figure object: {type(fig)}, size: {fig.get_size_inches()}")
            return fig, None
            
        except Exception as e:
            return None, f"Error generating plot {plot_type}: {str(e)}"

