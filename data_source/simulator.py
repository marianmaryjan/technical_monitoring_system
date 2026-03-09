import random


def generate_data(rows=2000, samples_per_run=200):

    data = []

    runs = rows // samples_per_run

    for run_id in range(runs):

        degradation_rate = random.uniform(0.6, 1.4)

        # każdy sensor może mieć lekki drift
        temp_drift = random.uniform(-0.01, 0.01)
        press_drift = random.uniform(-0.02, 0.02)
        vib_drift = random.uniform(-0.005, 0.005)

        # różne typy awarii
        failure_type = random.choice(["bearing", "overheat", "pressure_loss"])

        for i in range(samples_per_run):

            sample_number = i
            progress = i / samples_per_run

            # nieliniowa degradacja
            health = max(0, 1 - (progress ** 2) * degradation_rate)

            if health > 0.7:
                state = "normal"
            elif health > 0.4:
                state = "degraded"
            else:
                state = "failure"

            # noise rośnie wraz z degradacją
            noise_scale = 0.3 + (1 - health) * 0.7

            # bazowe sensory
            temperature = 20 + (1 - health) * 10
            vibration = 0.5 + (1 - health) * 8
            pressure = 100 - (1 - health) * 6

            # typ awarii wpływa na sensory
            if failure_type == "bearing":
                vibration += (1 - health) * 4
            elif failure_type == "overheat":
                temperature += (1 - health) * 6
            elif failure_type == "pressure_loss":
                pressure -= (1 - health) * 5

            # dodajemy drift
            temperature += i * temp_drift
            pressure += i * press_drift
            vibration += i * vib_drift

            # losowy noise
            temperature += random.gauss(0, noise_scale)
            pressure += random.gauss(0, noise_scale * 0.5)
            vibration += random.gauss(0, noise_scale)

            # sporadyczne anomalie (spikes)
            if random.random() < 0.01:
                vibration += random.uniform(3, 6)

            if random.random() < 0.005:
                temperature += random.uniform(2, 5)

            row = {
                "run_id": run_id,
                "sample_number": sample_number,
                "temperature": round(temperature, 2),
                "pressure": round(pressure, 2),
                "vibration": round(vibration, 2),
                "health": round(health, 4),
                "state": state
            }

            data.append(row)

    return data