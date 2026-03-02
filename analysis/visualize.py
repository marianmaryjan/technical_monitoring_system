import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def plot_sensor_data(csv_path):
    df = pd.read_csv(csv_path)
    df["sample"] = range(len(df))
    
    df = df.sort_values("sample")
    
    plt.figure(figsize=(12, 6))
    plt.plot(df["sample"], df["temperature"], label="Temperature")
    plt.plot(df["sample"], df["pressure"], label="Pressure")
    plt.plot(df["sample"], df["vibration"], label="Vibration")
    
    plt.xlabel("Sample number")
    plt.ylabel("Sensor values")
    plt.title("Sensor Data Over Time")
    plt.legend()
    plt.tight_layout()

    Path("plots").mkdir(exist_ok=True)
    output_path = Path("plots") / "sensor_plot.png"

    plt.savefig(output_path)
    plt.close()

    print("Plot saved to:", output_path)