# core/rules.py

def check_thresholds(sensor_data, thresholds):
    """
    Compares sensor data against defined thresholds.
    Returns status for each measurement: 'OK', 'WARNING', 'CRITICAL'
    """
    status = {}
    for key, value in sensor_data.items():
        if key not in thresholds:
            status[key] = "UNKNOWN"
            continue
        t_warning = thresholds[key]["warning"]
        t_critical = thresholds[key]["critical"]

        if value >= t_critical:
            status[key] = "CRITICAL"
        elif value >= t_warning:
            status[key] = "WARNING"
        else:
            status[key] = "OK"
    return status
