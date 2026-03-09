#!/usr/bin/env python
"""
Quick start script to train the ML model and test predictions.
Run this to get the system up and running with ML capabilities.
"""

from core.ml_predictor import MLPredictor
from data_source import simulator
import numpy as np


def quick_start():
    print("=" * 60)
    print("[ML] Technical Monitoring System - ML Quick Start")
    print("=" * 60)
    
    # Step 1: Train the model
    print("\n[TRAIN] Step 1: Training model on simulated data...")
    print("-" * 60)
    
    X_train = []
    y_train = []
    
    # Generate training data
    samples = 3000
    samples_per_run = 150
    data = simulator.generate_data(samples, samples_per_run)
    
    for row in data:
        X_train.append([
            row.get('temperature', 0),
            row.get('vibration', 0),
            row.get('pressure', 0)
        ])
        y_train.append(row.get('state', 'unknown'))
    
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    predictor = MLPredictor()
    predictor.train(X_train, y_train)
    
    # Step 2: Show feature importance
    print("\n[FEATURES] Feature Importance:")
    print("-" * 60)
    importance = predictor.get_feature_importance()
    if importance:
        for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
            bar = "*" * int(score * 10)
            print(f"{feature:15} {score:6.2%} {bar}")
    
    # Step 3: Test predictions
    print("\n[TEST] Step 2: Testing predictions on new data...")
    print("-" * 60)
    
    test_cases = [
        {"temperature": 20, "vibration": 0.5, "pressure": 100, "label": "Normal operation"},
        {"temperature": 25, "vibration": 3.0, "pressure": 95, "label": "Moderate degradation"},
        {"temperature": 30, "vibration": 6.0, "pressure": 85, "label": "Severe degradation"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        sensor_data = {k: v for k, v in test_case.items() if k != 'label'}
        result = predictor.predict(sensor_data)
        
        print(f"\n  Test {i}: {test_case['label']}")
        print(f"  - Sensor readings: T={sensor_data['temperature']}C, V={sensor_data['vibration']}g, P={sensor_data['pressure']}bar")
        print(f"  - Prediction: {result['prediction'].upper()} (confidence: {result['confidence']})")
        if 'probabilities' in result:
            probs = result['probabilities']
            print(f"  - Probabilities: Normal={probs['normal']} | Degraded={probs['degraded']} | Failure={probs['failure']}")
    
    print("\n" + "=" * 60)
    print("[OK] Quick start completed! Model is ready to use.")
    print("\nNext steps:")
    print("  1. Run: python main.py (to monitor with ML predictions)")
    print("  2. Run: python train_model.py (to train with more data)")
    print("=" * 60)


if __name__ == "__main__":
    quick_start()
