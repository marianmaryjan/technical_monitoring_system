"""
Demo script showing ML integration with monitoring system.
Shows first 5 predictions side-by-side.
"""

from data_source import simulator
import yaml
from core import rules
from core.ml_predictor import MLPredictor
from data_storage import csv_writer

def demo():
    print("=" * 80)
    print("[DEMO] Technical Monitoring System with ML Predictions")
    print("=" * 80)
    
    # Load thresholds
    with open("config/thresholds.yaml") as file:
        thresholds = yaml.safe_load(file)
    
    writer = csv_writer.CSVWriter()
    predictor = MLPredictor()
    
    # Generate sample data
    samples = 500
    samples_per_run = 100
    data = simulator.generate_data(samples, samples_per_run)
    
    print("\n[INFO] Monitoring sensor data with both threshold-based and ML predictions:\n")
    print(f"{'#':>3} | {'Temp':>5} | {'Vibr':>5} | {'Pres':>5} | {'Thresholds':^25} | {'ML Prediction':^30}")
    print("-" * 120)
    
    count = 0
    for row in data:
        if count >= 15:  # Show only first 15 readings
            break
        
        # Threshold-based check
        status = rules.check_thresholds(row, thresholds)
        status_str = ",".join([f"{k}:{v}" for k, v in status.items()])
        
        # ML prediction
        ml_result = predictor.predict(row)
        ml_str = f"{ml_result['prediction'].upper()} ({ml_result['confidence']})"
        
        # Print row
        print(f"{count+1:3d} | {row['temperature']:5.1f} | {row['vibration']:5.1f} | {row['pressure']:5.1f} | {status_str:^25} | {ml_str:^30}")
        
        writer.write_row(row)
        count += 1
    
    print("\n" + "=" * 80)
    print("[OK] Demo completed!")
    print("\nKey differences:")
    print("  - Thresholds: Binary rule-based (OK/WARNING/CRITICAL)")
    print("  - ML Model: Probabilistic predictions with confidence scores")
    print("  - Together: Both methods provide complementary insights")
    print("=" * 80)


if __name__ == "__main__":
    demo()
