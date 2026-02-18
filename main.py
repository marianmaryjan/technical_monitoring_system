from data_source import simulator
import yaml
from core import rules
from data_storage import csv_writer

def main():
    # 1️⃣ wczytanie progów z YAML
    with open("config/thresholds.yaml") as file:
        thresholds = yaml.safe_load(file)
    writer = csv_writer.CSVWriter()  # inicjalizacja CSVWriter
    # 2️⃣ generujemy kilka danych
    data = simulator.generate_data(5)  # np. 5 wierszy danych

    for row in data:
        print("Sensor data:", row)
        status = rules.check_thresholds(row, thresholds)
        print("Status:", status)
        print("-" * 40)
        writer.write_row(row)



if __name__ == "__main__":
    main()
