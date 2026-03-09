"""
Training script for the machine learning model.
Generates sensor data and trains the predictor.
"""

import sys
from data_source import simulator
from core.ml_predictor import MLPredictor
import numpy as np


def prepare_training_data():
    """
    Generate and prepare training data for ML model.
    
    Returns:
        X_train: Features (temperature, vibration, pressure)
        y_train: Labels (normal, degraded, failure)
    """
    print("📊 Generating training data...")
    
    # Generate training samples
    samples = 5000
    samples_per_run = 100
    data = simulator.generate_data(samples, samples_per_run)
    
    X_train = []
    y_train = []
    
    for row in data:
        # Extract features
        features = [
            row.get('temperature', 0),
            row.get('vibration', 0),
            row.get('pressure', 0)
        ]
        X_train.append(features)
        
        # Extract label (state)
        state = row.get('state', 'unknown')
        y_train.append(state)
    
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    print(f"✓ Generated {len(X_train)} training samples")
    print(f"  - Normal: {np.sum(y_train == 'normal')}")
    print(f"  - Degraded: {np.sum(y_train == 'degraded')}")
    print(f"  - Failure: {np.sum(y_train == 'failure')}")
    
    return X_train, y_train


def main():
    print("=" * 50)
    print("[ML] Machine Learning Model Training")
    print("=" * 50)
    
    # Prepare data
    X_train, y_train = prepare_training_data()
    
    # Train model
    print("\n[TRAIN] Training model...")
    predictor = MLPredictor()
    predictor.train(X_train, y_train)
    
    # Display feature importance
    print("\n[INFO] Feature Importance:")
    importance = predictor.get_feature_importance()
    if importance:
        for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
            print(f"  * {feature}: {score}")
    
    print("\n" + "=" * 50)
    print("[OK] Training completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
