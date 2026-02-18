import csv
from datetime import datetime
from pathlib import Path


class CSVWriter:
    def __init__(self, filename="sensor_data.csv"):
        Path("data").mkdir(exist_ok=True)
        self.filepath = Path("data") / filename
        self._init_file()

    def _init_file(self):
        if not self.filepath.exists():
            with open(self.filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "temperature", "pressure", "vibration"])

    def write_row(self, row):
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                row["temperature"],
                row["pressure"],
                row["vibration"],
            ])
