## Requirements

We run this project with Python 3.10+.
Data is hourly crypto OHLCV.
Training period is 2018–2020, and test period is full 2021.

## Python packages

- pandas
- numpy
- scikit-learn
- matplotlib
- statsmodels
- joblib

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Data requirements

- input file must be named `prices.csv` in the project root
- must include a datetime column (`date`, `datetime`, `timestamp`, or `time`)
- must include close price (`close` or a compatible alias handled by `utils.py`)