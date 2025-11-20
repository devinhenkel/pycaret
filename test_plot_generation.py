#!/usr/bin/env python3
"""
Test script to verify plot generation works correctly.
This tests the visualization module without running the full Gradio app.
"""

import sys
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from src.modules.visualization import VisualizationManager

def test_plot_generation():
    """Test that plots can be generated and returned correctly."""
    
    print("=" * 60)
    print("Testing Plot Generation")
    print("=" * 60)
    
    # Create a simple dataset
    print("\n1. Creating test dataset...")
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    
    print(f"   ✓ Dataset created: {df.shape}")
    
    # Initialize PyCaret setup (Classification)
    print("\n2. Initializing PyCaret setup...")
    try:
        from pycaret.classification import setup as clf_setup, create_model
        
        setup = clf_setup(
            data=df,
            target='target',
            session_id=123,
            verbose=False,
            system=False  # Prevent display
        )
        print("   ✓ PyCaret setup initialized")
    except Exception as e:
        print(f"   ✗ Setup failed: {e}")
        return False
    
    # Train a simple model
    print("\n3. Training a simple model...")
    try:
        model = create_model('dt', verbose=False)  # Decision Tree
        print(f"   ✓ Model trained: {type(model)}")
    except Exception as e:
        print(f"   ✗ Model training failed: {e}")
        return False
    
    # Test plot generation
    print("\n4. Testing plot generation...")
    viz_manager = VisualizationManager()
    viz_manager.set_problem_type('classification')
    viz_manager.set_setup(setup)
    
    # Get available plots
    available_plots = viz_manager.get_available_plots()
    print(f"   Available plots: {available_plots}")
    
    # Test generating a confusion matrix
    plot_type = 'confusion_matrix'
    print(f"\n5. Generating '{plot_type}' plot...")
    try:
        plot_obj, error = viz_manager.generate_plot(model, plot_type)
        
        if error:
            print(f"   ✗ Plot generation failed: {error}")
            return False
        
        if plot_obj is None:
            print(f"   ✗ Plot object is None!")
            return False
        
        print(f"   ✓ Plot generated successfully!")
        print(f"   ✓ Plot type: {type(plot_obj)}")
        
        # Check if it's a matplotlib figure
        if hasattr(plot_obj, 'savefig'):
            print(f"   ✓ Plot is a matplotlib figure")
            print(f"   ✓ Figure has {len(plot_obj.get_axes())} axes")
            print(f"   ✓ Figure size: {plot_obj.get_size_inches()}")
        elif hasattr(plot_obj, 'write_html'):
            print(f"   ✓ Plot is a Plotly figure")
        else:
            print(f"   ⚠ Plot is neither matplotlib nor Plotly: {type(plot_obj)}")
        
        # Verify the plot object is valid for Gradio
        print("\n6. Verifying plot is Gradio-compatible...")
        if hasattr(plot_obj, 'savefig') or hasattr(plot_obj, 'write_html'):
            print(f"   ✓ Plot object is compatible with Gradio's gr.Plot()")
            return True
        else:
            print(f"   ✗ Plot object may not be compatible with Gradio")
            return False
            
    except Exception as e:
        import traceback
        print(f"   ✗ Exception during plot generation:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PyCaret Plot Generation Test")
    print("=" * 60)
    
    success = test_plot_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\nPlots should now render correctly in the Gradio UI.")
        print("Next steps:")
        print("1. Run: python main.py")
        print("2. Upload a dataset")
        print("3. Complete the workflow and try generating plots")
        sys.exit(0)
    else:
        print("❌ TESTS FAILED")
        print("=" * 60)
        print("\nPlots may not render correctly. Check the errors above.")
        sys.exit(1)
