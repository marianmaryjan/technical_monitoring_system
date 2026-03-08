from data_source import simulator
import yaml
from core import rules
from data_storage import csv_writer
from analysis import visualize

def main():
    # 1️⃣ wczytanie progów z YAML
    with open("config/thresholds.yaml") as file:
        thresholds = yaml.safe_load(file)
    writer = csv_writer.CSVWriter()  # inicjalizacja CSVWriter
    # 2️⃣ generujemy kilka danych
    samples = 2000
    samples_per_run = 200
    data = simulator.generate_data(samples, samples_per_run)  # np. 5 wierszy danych

    for row in data:
        print("Sensor data:", row)
        status = rules.check_thresholds(row, thresholds)
        print("Status:", status)
        print("-" * 40)
        writer.write_row(row)
    
    for run_id in range(samples // samples_per_run):
        visualize.plot_sensor_data("data/sensor_data.csv", run_id=run_id)

if __name__ == "__main__":
    main()