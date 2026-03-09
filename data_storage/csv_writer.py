import csv
from pathlib import Path


class CSVWriter:
    def __init__(self, filename="sensor_data.csv", overwrite=True):
        Path("data").mkdir(exist_ok=True)
        self.filepath = Path("data") / filename
        self.header = [
            "run_id",
            "sample_number",
            "temperature",
            "pressure",
            "vibration",
            "health",
            "state",
            # optional ML outputs
            "ml_prediction",
            "ml_confidence"
        ]
        self._init_file(overwrite)
    
    def _init_file(self, overwrite):

        if overwrite or not self.filepath.exists():
            with open(self.filepath, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.header)

    def write_row(self, row):
        # ensure we write values for all header columns, using empty string if missing
        values = [row.get(col, "") for col in self.header]
        with open(self.filepath, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(values)