# Copilot Instructions for Technical Monitoring System

## Overview
This project is a Python-based system that simulates technical sensor data, monitors it against configurable thresholds, and reports status. It is modular and designed for automation and industrial monitoring projects.

## Architecture
- **Main Components**:
  - **data_source**: Contains the `simulator.py` which generates simulated sensor data (temperature, pressure, vibration).
  - **core**: Logic and decision modules (currently empty).
  - **reporting**: Responsible for logging and reporting (currently empty).
  - **config**: Holds configuration files (currently empty).
  - **main.py**: Entry point for the application.

## Developer Workflows
- **Running the System**:
  1. Activate the virtual environment:
     ```bash
     source venv/Scripts/activate  # Windows Git Bash
     ```
  2. Install requirements:
     ```bash
     pip install pyyaml
     ```
  3. Run the system:
     ```bash
     python main.py
     ```

## Project Conventions
- The project uses a modular structure, allowing for easy expansion in the future.
- Sensor data is generated in `data_source/simulator.py` using the `generate_data` function, which creates random values for temperature, pressure, and vibration.

## Integration Points
- The system integrates with external libraries such as PyYAML for configuration management.

## Example Usage
To generate sensor data, call the `generate_data` function from `data_source/simulator.py`:
```python
from data_source.simulator import generate_data

sensor_data = generate_data(rows=10)
print(sensor_data)
```

## Conclusion
This document serves as a guide for AI coding agents to understand the structure and workflows of the Technical Monitoring System. For further details, refer to the respective modules and files as needed.