# Technical Monitoring System

This is a Python-based system that simulates technical sensor data, monitors it against configurable thresholds, and reports status. The system is modular and designed for automation and industrial monitoring projects.

## Project Structure
technical_monitoring_system/
├── data_source/ # simulator of sensor data
├── core/ # logic and decision modules
├── reporting/ # logging and reporting
├── config/ # configuration files (YAML)
└── main.py # entry point

## Features
- Generates simulated sensor data (temperature, pressure, vibration)
- Compares readings against configurable warning and critical thresholds
- Prints status of each sensor reading
- Modular structure ready for expansion (logging, automated reactions)

## Requirements

- Python 3.14+
- PyYAML library

## How to run

```bash
# activate virtual environment
source venv/Scripts/activate  # Windows Git Bash
# install requirements
pip install pyyaml
# run system
python main.py
