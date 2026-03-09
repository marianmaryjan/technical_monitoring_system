from data_source import simulator
import yaml
from core import rules
from core.ml_predictor import MLPredictor
from data_storage import csv_writer
from analysis import visualize

def main():
    # 1️⃣ wczytanie progów z YAML
    with open("config/thresholds.yaml") as file:
        thresholds = yaml.safe_load(file)
    writer = csv_writer.CSVWriter()  # inicjalizacja CSVWriter
    predictor = MLPredictor()  # inicjalizacja ML predictora
    
    # 2️⃣ generujemy kilka danych
    samples = 2000
    samples_per_run = 200
    data = simulator.generate_data(samples, samples_per_run)  # np. 5 wierszy danych

    for row in data:
        print("Sensor data:", row)
        status = rules.check_thresholds(row, thresholds)
        print("Threshold-based Status:", status)
        
        # 3️⃣ ML prediction
        ml_result = predictor.predict(row)
        print(f"ML Prediction: {ml_result['prediction']} (confidence: {ml_result['confidence']})")
        if 'probabilities' in ml_result:
            print(f"  Probabilities: {ml_result['probabilities']}")
        
        # attach ML info to row so CSV can store it
        row["ml_prediction"] = ml_result['prediction']
        row["ml_confidence"] = ml_result['confidence']
        
        print("-" * 40)
        writer.write_row(row)
    
    for run_id in range(samples // samples_per_run):
        visualize.plot_sensor_data("data/sensor_data.csv", run_id=run_id)

if __name__ == "__main__":
    main()