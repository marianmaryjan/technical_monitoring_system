import csv
from pathlib import Path


class CSVWriter:
    def __init__(self, filename="sensor_data.csv", overwrite=True):
        Path("data").mkdir(exist_ok=True)
        self.filepath = Path("data") / filename
        self._init_file(overwrite)

    def _init_file(self, overwrite):

        if overwrite or not self.filepath.exists():
            with open(self.filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "run_id",
                    "sample_number",
                    "temperature",
                    "pressure",
                    "vibration",
                    "health",
                    "state"
                ])

    def write_row(self, row):
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                row["run_id"],
                row["sample_number"],
                row["temperature"],
                row["pressure"],
                row["vibration"],
                row["health"],
                row["state"]
            ])