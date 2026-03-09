# Technical Monitoring System

This is a Python-based system that simulates technical sensor data, monitors it against configurable thresholds, and reports status. The system is modular and designed for automation and industrial monitoring projects.

## Project Structure
technical_monitoring_system/
├── data_source/ # simulator of sensor data
├── core/ # logic and decision modules
├── reporting/ # logging and reporting
├── config/ # configuration files (YAML)
└── main.py # entry point

## Features
- **Sensor Data Simulation**: Generates realistic simulated sensor data (temperature, pressure, vibration)
- **Threshold-Based Monitoring**: Compares readings against configurable warning and critical thresholds
- **Machine Learning Predictions**: Predicts machine state (normal, degraded, failure) using trained ML model
- **Data Storage**: Stores all readings in CSV format for analysis
- **Visualization**: Generates plots of sensor data over time
- **Modular Architecture**: Clean, expandable design for easy modifications

## Machine Learning Integration

The system now includes a Random Forest-based machine learning model that predicts machine state based on sensor readings:

### How it works:
1. **Training**: The ML model learns patterns from simulated sensor data
2. **Prediction**: For each new sensor reading, the model predicts the machine state with confidence scores
3. **Feature Importance**: Temperature, vibration, and pressure are weighted by their importance to the prediction

### Files:
- `core/ml_predictor.py` - ML prediction engine
- `train_model.py` - Script to train the model
- `quick_start.py` - Interactive demo of ML capabilities
- `core/models/` - Stores trained model and scaler

## Requirements

- Python 3.8+
- Libraries: PyYAML, scikit-learn, numpy, matplotlib

## Installation & Quick Start

```bash
# 1. activate virtual environment
source venv/Scripts/activate  # Windows Git Bash

# 2. install requirements
pip install -r requirements.txt

# 3. train the ML model (run once)
python quick_start.py

# 4. run the monitoring system with ML predictions
python main.py

# OR for full training with more data:
python train_model.py
