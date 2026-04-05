## Requirements

we run this project with python 3.10+  
we use hourly crypto OHLCV data  
we train on 2018-2020 and test on full 2021

### python packages

- pandas
- numpy
- scikit-learn
- matplotlib
- statsmodels
- joblib

### install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### data requirements

- input file name: `prices.csv` in project root
- must contain a datetime column (`date`, `datetime`, `timestamp`, or `time`)
- must contain close price (`close` or a compatible alias handled by `utils.py`)