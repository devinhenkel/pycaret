"""
Script to create sample datasets for testing the PyCaret ML Workflow Manager.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Create output directory
output_dir = Path(__file__).parent
output_dir.mkdir(parents=True, exist_ok=True)


def create_classification_sample():
    """Create a sample classification dataset."""
    np.random.seed(42)
    n_samples = 100
    
    # Generate features
    data = {
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'feature3': np.random.randn(n_samples),
        'feature4': np.random.randn(n_samples),
        'feature5': np.random.randn(n_samples),
    }
    
    # Create target based on features (simple classification problem)
    # Target is 0 or 1 based on feature combination
    target = ((data['feature1'] > 0) & (data['feature2'] > 0)).astype(int)
    
    # Add some noise
    noise = np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2])
    target = np.where(noise == 1, 1 - target, target)
    
    data['target'] = target
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_path = output_dir / 'classification_sample.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Created classification sample: {output_path}")
    print(f"   Shape: {df.shape}")
    print(f"   Target distribution:\n{df['target'].value_counts()}")
    
    return df


def create_regression_sample():
    """Create a sample regression dataset."""
    np.random.seed(42)
    n_samples = 100
    
    # Generate features
    data = {
        'feature1': np.random.randn(n_samples),
        'feature2': np.random.randn(n_samples),
        'feature3': np.random.randn(n_samples),
        'feature4': np.random.randn(n_samples),
    }
    
    # Create target as linear combination of features + noise
    target = (
        2 * data['feature1'] +
        1.5 * data['feature2'] -
        0.5 * data['feature3'] +
        0.3 * data['feature4'] +
        np.random.randn(n_samples) * 0.5
    )
    
    data['target'] = target
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_path = output_dir / 'regression_sample.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Created regression sample: {output_path}")
    print(f"   Shape: {df.shape}")
    print(f"   Target stats: mean={df['target'].mean():.2f}, std={df['target'].std():.2f}")
    
    return df


if __name__ == "__main__":
    print("Creating sample datasets for testing...\n")
    create_classification_sample()
    print()
    create_regression_sample()
    print("\n✅ All sample datasets created successfully!")
    print(f"   Location: {output_dir}")

