import random


def generate_data(rows=2000, samples_per_run=200):

    data = []

    runs = rows // samples_per_run

    for run_id in range(runs):

        # każda maszyna zużywa się trochę inaczej
        degradation_rate = random.uniform(0.6, 1.4)

        for i in range(samples_per_run):

            sample_number = i

            progress = i / samples_per_run

            # nieliniowa degradacja (powoli -> szybko)
            health = max(0, 1 - (progress ** 2) * degradation_rate)

            if health > 0.7:
                state = "normal"
            elif health > 0.4:
                state = "degraded"
            else:
                state = "failure"

            # temperatura rośnie przy zużyciu
            temperature = round(
                20 + (1 - health) * 10 + random.gauss(0, 0.4), 2
            )

            # wibracje mocno rosną przy degradacji
            vibration = round(
                0.5 + (1 - health) * 8 + random.gauss(0, 0.5), 2
            )

            # ciśnienie lekko spada
            pressure = round(
                100 - (1 - health) * 6 + random.gauss(0, 0.3), 2
            )

            row = {
                "run_id": run_id,
                "sample_number": sample_number,
                "temperature": temperature,
                "pressure": pressure,
                "vibration": vibration,
                "health": round(health, 4),
                "state": state
            }

            data.append(row)

    return data