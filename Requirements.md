## Requirements

we run this project on python 3.10+  
we use hourly crypto OHLCV data with a valid datetime column and close price column  
we train on 2018 to 2020 and test on full year 2021

### python packages

- pandas
- numpy
- scikit-learn
- matplotlib
- statsmodels
- joblib

### install

```bash
python3 -m pip install -r requirements.txt
```

### data requirement

the input file must be named `prices.csv` and placed in project root  
accepted datetime column names include `date datetime timestamp time`  
close price must be available as `close` or compatible alias handled by `utils.py`