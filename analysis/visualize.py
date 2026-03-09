import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_sensor_data(csv_path, run_id=0):

    df = pd.read_csv(csv_path)

    # wybieramy jedną maszynę
    df = df[df["run_id"] == run_id].copy()
    df = df.sort_values("sample_number")

    # jeśli w danych nie ma kolumn ML, spróbuj je wygenerować przy użyciu predictor
    if "ml_prediction" not in df.columns:
        from core.ml_predictor import MLPredictor
        predictor = MLPredictor()
        preds = []
        confidences = []
        for _, row in df.iterrows():
            res = predictor.predict(row)
            preds.append(res.get("prediction", "unknown"))
            confidences.append(res.get("confidence", 0.0))
        df["ml_prediction"] = preds
        df["ml_confidence"] = confidences

    # tworzymy 4 panele z wspólną osią X (ostatni dla ML)
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    ax_temp, ax_press, ax_vib, ax_ml = axes

    # rysowanie linii
    ax_temp.plot(df["sample_number"], df["temperature"], label="Temperature", color="tab:red")
    ax_press.plot(df["sample_number"], df["pressure"], label="Pressure", color="tab:blue")
    ax_vib.plot(df["sample_number"], df["vibration"], label="Vibration", color="tab:green")

    # kolory stanów
    state_colors = {
        "normal": "green",
        "degraded": "orange",
        "failure": "red"
    }

    # rysowanie stref stanu (na pierwszych trzech panelach)
    current_state = None
    start = None

    for _, row in df.iterrows():

        if row["state"] != current_state:

            if current_state is not None:
                for ax in (ax_temp, ax_press, ax_vib):
                    ax.axvspan(
                        start,
                        row["sample_number"],
                        color=state_colors[current_state],
                        alpha=0.1
                    )

            current_state = row["state"]
            start = row["sample_number"]

    # ostatni fragment dla stanu
    if current_state is not None:
        for ax in (ax_temp, ax_press, ax_vib):
            ax.axvspan(
                start,
                df["sample_number"].iloc[-1],
                color=state_colors[current_state],
                alpha=0.1
            )

    # ---- ML prediction panel ----
    ml_colors = {
        "normal": "#88c999",
        "degraded": "#ffcc66",
        "failure": "#e06666",
        "unknown": "#cccccc"
    }
    current_ml = None
    start_ml = None
    for _, row in df.iterrows():
        ml_state = row.get("ml_prediction", "unknown")
        if ml_state != current_ml:
            if current_ml is not None:
                ax_ml.axvspan(start_ml, row["sample_number"], color=ml_colors[current_ml], alpha=0.3)
            current_ml = ml_state
            start_ml = row["sample_number"]
    if current_ml is not None:
        ax_ml.axvspan(start_ml, df["sample_number"].iloc[-1], color=ml_colors[current_ml], alpha=0.3)

    # opisy osi
    ax_temp.set_ylabel("Temperature")
    ax_press.set_ylabel("Pressure")
    ax_vib.set_ylabel("Vibration")
    ax_ml.set_ylabel("ML State")
    ax_ml.set_yticks([])  # wykres kategorii

    ax_vib.set_xlabel("Sample number (time)")

    # tytuł
    fig.suptitle(f"Machine Monitoring - Run {run_id}")

    # grid and legends
    for ax in axes:
        ax.grid(True)
    # standard legend for first three axes is handled above; add ML legend specifically
    import matplotlib.patches as mpatches
    ml_patches = [mpatches.Patch(color=col, label=state.capitalize()) for state, col in ml_colors.items()]
    ax_ml.legend(handles=ml_patches, loc="upper left")

    plt.tight_layout()

    Path("plots").mkdir(exist_ok=True)
    output_path = Path("plots") / f"sensor_plot_run_{run_id}.png"

    plt.savefig(output_path)
    plt.close()

    print("Plot saved to:", output_path)