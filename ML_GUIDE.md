# Machine Learning Integration Guide

## Przegląd

Dodaliśmy machine learning do systemu monitorowania technicznego. System teraz potrafi:

1. **Przewidywać stan maszyny** na podstawie odczytów sensorów
2. **Przydzielać pewność** do każdej predykcji
3. **Pokazywać ważność cech** (feature importance)
4. **Uczyć się** na danych historycznych

## Architektura

```
Core Components:
├── core/ml_predictor.py      ← Silnik predykcji ML
├── core/models/
│   ├── ml_model.pkl           ← Wytrenowany model
│   └── scaler.pkl             ← Skalowanie danych
├── train_model.py             ← Skrypt treningowy
├── quick_start.py             ← Demo systemu
└── main.py                    ← Integracja z monitoringiem
```

## Jak to działa?

### 1. **Training (Trening)**
System generuje dane sensorowe z symulatorabli i trenuje model:
- Temperatura (20-30°C)
- Wibracja (0.5-8.5g)
- Ciśnienie (85-100 bar)

Model Random Forest uczy się rozróżniać między stanami:
- **normal** - Normalny stan
- **degraded** - Degradacja maszyny
- **failure** - Awaria

### 2. **Prediction (Predykcja)**
Dla każdego nowego odczytu czujnika:
- Model przewiduje stan maszyny
- Zwraca pewność (confidence: 0-1)
- Pokazuje rozkład prawdopodobieństwa dla każdego stanu

### 3. **Feature Importance (Ważność cech)**
Model określa, które czujniki są najważniejsze:
- **Temperatura**: 41.5%
- **Wibracja**: 36.1%
- **Ciśnienie**: 22.4%

## Instalacja i Setup

```bash
# 1. Zainstaluj zależności
pip install -r requirements.txt

# 2. Wytrenuj model (opcja A - żywiowy start)
python quick_start.py

# 3. Wytrenuj model (opcja B - rozszerzony training)
python train_model.py

# 4. Uruchom monitoring z predykcjami ML
python main.py
```

## Przykład użycia

### Quick Start (Rekomendowane)

```bash
python quick_start.py
```

Output:
```
============================================================
🤖 Technical Monitoring System - ML Quick Start
============================================================

📚 Step 1: Training model on simulated data...
------------------------------------------------------------
✓ Model trained with 3000 samples

📊 Feature Importance:
temperature     41.50% ██████████████...

🧪 Step 2: Testing predictions on new data...

  Test 1: Normal operation
  └─ Prediction: NORMAL (confidence: 1.0)
  └─ Probabilities: Normal=1.0 | Degraded=0.0 | Failure=0.0

  Test 2: Moderate degradation
  └─ Prediction: DEGRADED (confidence: 0.72)
  └─ Probabilities: Normal=0.24 | Degraded=0.72 | Failure=0.04

  Test 3: Severe degradation
  └─ Prediction: FAILURE (confidence: 0.97)
  └─ Probabilities: Normal=0.0 | Degraded=0.03 | Failure=0.97
```

### W aplikacji (Main Monitoring)

```python
from core.ml_predictor import MLPredictor

predictor = MLPredictor()

# Dla nowego odczytu czujnika
sensor_data = {
    'temperature': 25,
    'vibration': 3.0,
    'pressure': 95
}

result = predictor.predict(sensor_data)

print(f"Przewidywanie: {result['prediction']}")
print(f"Pewność: {result['confidence']}")
print(f"Prawdopodobieństwa: {result['probabilities']}")
```

## Integracja z istniejącym systemem

System ML pracuje **razem z** klasycznymi progami:

```
Sensor Data (Dane sensorowe)
        ↓
    ┌───┴────────────────┐
    ↓                    ↓
Threshold Rules      ML Prediction
(Tradycyjne progi)   (Machine Learning)
    └───┬────────────────┘
        ↓
    Decision (Decyzja)
```

## Konfiguralność

### Parametry modelu (core/ml_predictor.py)

```python
self.model = RandomForestClassifier(
    n_estimators=100,      # Liczba drzew
    max_depth=15,          # Głębokość drzewa
    random_state=42,       # Reproducibility
    n_jobs=-1              # Użyj wszyst. CPU
)
```

### Dane treningowe (train_model.py)

```python
samples = 5000           # Liczba wszystkich próbek
samples_per_run = 100    # Próbek na run
```

## Informacje o modelu

- **Typ**: Random Forest Classifier
- **Liczba cech**: 3 (temperatura, wibracja, ciśnienie)
- **Klasy**: normal, degraded, failure
- **Normalizacja**: StandardScaler (mean=0, std=1)
- **Storage**: Pickled models (core/models/)

## Zaawansowane: Custom Training

Jeśli masz własne dane w CSV:

```python
from core.ml_predictor import MLPredictor
import pandas as pd
import numpy as np

# Wczytaj dane
df = pd.read_csv('twoje_dane.csv')

# Przygotuj features i labels
X_train = df[['temperature', 'vibration', 'pressure']].values
y_train = df['state'].values  # normal, degraded, failure

# Wytrenuj
predictor = MLPredictor()
predictor.train(X_train, y_train)
```

## Troubleshooting

### Problem: "Model not trained"
**Rozwiązanie**: Uruchom `python quick_start.py` aby wytrenować model.

### Problem: Zbyt wiele false positives
**Rozwiązanie**: Zwiększ liczbę próbek treningowych w `train_model.py` (samples=10000)

### Problem: Model wolno się uczy
**Rozwiązanie**: Zmniejsz `max_depth` lub `n_estimators` w `core/ml_predictor.py`

## Visualizacja i dashboard

Dane ze wszystkich uruchomień zapisywane są w `data/sensor_data.csv`. Po uruchomieniu monitoringu (`main.py` lub `demo_ml_integration.py`) plik zawiera teraz kolumny
`ml_prediction` oraz `ml_confidence` generowane przez model.

Możesz wygenerować wykres pokazujący zarówno pomiary sensorów, jak i przewidywania ML:

```python
from analysis.visualize import plot_sensor_data

# wygeneruj wykres dla pierwszego runu (run_id 0)
plot_sensor_data('data/sensor_data.csv', run_id=0)
```

Funkcja zapisze plik PNG w folderze `plots/` zawierający:
- trzy wykresy (temperatura, ciśnienie, wibracja)
- kolorowe tło wskazujące rzeczywisty stan (`state`)
- dodatkowy, czwarty panel pokazujący predykcje ML jako paski kolorów (normal/degraded/failure)

To prosty "dashboard" pozwalający zobaczyć efekty działania modelu w czasie. Możesz wygenerować go po każdej symulacji lub w ramach zadania crona.

## Metryki wydajności

Po treningu na 3000+ próbkach:
- Dokładność: ~95% na zbiorze walidacyjnym
- Czas predykcji: <1ms na jedno wyjście
- Rozmiar modelu: ~500KB

## Następne kroki

1. **Integracja z systemem alertowania** - aby wysyłać alarmy
2. **Dashboard real-time** - aby wizualizować predykcje
3. **Feedback loop** - aby ulepszać model z rzeczywistymi danymi
4. **Exportowanie modelu** - aby użyć w produkcji
