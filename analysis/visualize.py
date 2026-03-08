import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_sensor_data(csv_path, run_id=0):

    df = pd.read_csv(csv_path)

    # wybieramy jedną maszynę (run)
    df = df[df["run_id"] == run_id].copy()

    df = df.sort_values("sample_number")

    plt.figure(figsize=(12, 6))

    # linie sensorów
    plt.plot(df["sample_number"], df["temperature"], label="Temperature")
    plt.plot(df["sample_number"], df["pressure"], label="Pressure")
    plt.plot(df["sample_number"], df["vibration"], label="Vibration")

    # kolory stanów
    state_colors = {
        "normal": "green",
        "degraded": "orange",
        "failure": "red"
    }

    # rysowanie kolorowych stref stanu maszyny
    current_state = None
    start = None

    for _, row in df.iterrows():

        if row["state"] != current_state:

            if current_state is not None:
                plt.axvspan(
                    start,
                    row["sample_number"],
                    color=state_colors[current_state],
                    alpha=0.1
                )

            current_state = row["state"]
            start = row["sample_number"]

    # ostatni fragment
    if current_state is not None:
        plt.axvspan(
            start,
            df["sample_number"].iloc[-1],
            color=state_colors[current_state],
            alpha=0.1
        )

    plt.xlabel("Sample number (time)")
    plt.ylabel("Sensor values")
    plt.title(f"Machine Monitoring - Run {run_id}")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    Path("plots").mkdir(exist_ok=True)
    output_path = Path("plots") / f"sensor_plot_run_{run_id}.png"

    plt.savefig(output_path)
    plt.close()

    print("Plot saved to:", output_path)