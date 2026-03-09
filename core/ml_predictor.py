"""
Machine Learning module for predicting machine state based on sensor readings.
Uses scikit-learn for classification.
"""

import pickle
import os
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np


class MLPredictor:
    """
    Predicts machine state (normal, degraded, failure) based on sensor data.
    """
    
    MODEL_PATH = "core/models/ml_model.pkl"
    SCALER_PATH = "core/models/scaler.pkl"
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.is_trained = False
        self._ensure_model_dir()
        self._load_model()
    
    def _ensure_model_dir(self):
        """Create models directory if it doesn't exist."""
        os.makedirs("core/models", exist_ok=True)
    
    def _load_model(self):
        """Load pre-trained model and scaler if available."""
        if os.path.exists(self.MODEL_PATH) and os.path.exists(self.SCALER_PATH):
            try:
                with open(self.MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.SCALER_PATH, 'rb') as f:
                    self.scaler = pickle.load(f)
                self.is_trained = True
                print("[OK] Model loaded from disk")
            except Exception as e:
                print(f"[WARNING] Failed to load model: {e}")
    
    def train(self, X_train, y_train):
        """
        Train the ML model.
        
        Args:
            X_train: Training features (array-like, shape (n_samples, n_features))
            y_train: Training labels (array-like, shape (n_samples,))
        """
        # Initialize scaler and model
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train Random Forest classifier
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_scaled, y_train)
        self.is_trained = True
        
        # Save model and scaler
        self._save_model()
        print(f"[OK] Model trained with {len(X_train)} samples")
    
    def _save_model(self):
        """Save trained model and scaler to disk."""
        try:
            with open(self.MODEL_PATH, 'wb') as f:
                pickle.dump(self.model, f)
            with open(self.SCALER_PATH, 'wb') as f:
                pickle.dump(self.scaler, f)
            print("[OK] Model saved to disk")
        except Exception as e:
            print(f"[WARNING] Failed to save model: {e}")
    
    def predict(self, sensor_data):
        """
        Predict machine state based on sensor readings.
        
        Args:
            sensor_data: Dict with keys 'temperature', 'vibration', 'pressure'
            
        Returns:
            Dict with 'prediction' and 'confidence'
        """
        if not self.is_trained or self.model is None or self.scaler is None:
            return {
                'prediction': 'unknown',
                'confidence': 0.0,
                'error': 'Model not trained. Run training first.'
            }
        
        try:
            # Extract features in correct order
            features = np.array([[
                sensor_data.get('temperature', 0),
                sensor_data.get('vibration', 0),
                sensor_data.get('pressure', 0)
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            
            # Get confidence (max probability)
            probabilities = self.model.predict_proba(features_scaled)[0]
            confidence = float(np.max(probabilities))
            
            return {
                'prediction': prediction,
                'confidence': round(confidence, 2),
                'probabilities': {
                    'normal': round(probabilities[np.where(self.model.classes_ == 'normal')[0][0]], 2),
                    'degraded': round(probabilities[np.where(self.model.classes_ == 'degraded')[0][0]], 2),
                    'failure': round(probabilities[np.where(self.model.classes_ == 'failure')[0][0]], 2),
                }
            }
        except Exception as e:
            return {
                'prediction': 'error',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_feature_importance(self):
        """Get feature importance from trained model."""
        if not self.is_trained or self.model is None:
            return None
        
        features = ['temperature', 'vibration', 'pressure']
        importances = self.model.feature_importances_
        
        return {
            features[i]: round(float(importance), 3)
            for i, importance in enumerate(importances)
        }
