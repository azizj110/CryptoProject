# Crypto Project — ML Trading Pipeline

We build and evaluate a machine-learning trading strategy on crypto time series using a fixed, script-based pipeline.

## What this project does

- Engineers features from OHLCV data
- Builds trend-scanning labels
- Trains a Random Forest classifier
- Evaluates classification quality
- Runs a backtest (strategy vs buy-and-hold)
- Exports feature importance (MDI + PFI)
- Supports **SAFE** and **Aggressive** strategy profiles, with optional shorting

---

## Project structure

- `config.py` — global config (dates, costs, thresholds, mode flags)
- `mode_profile.py` — SAFE/Aggressive parameter profiles
- `utils.py` — shared helpers (loading prices, RSI, bars/year, etc.)
- `01_feature_engineering.py`
- `02_labeling_trend_scanning.py`
- `03_model_development.py`
- `04_feature_importance.py`
- `05_model_evaluation.py`
- `06_backtest_optional.py`
- `run_all.py` — runs the pipeline in order
- `test.py` — signal/position diagnostics
- `analysis.md` — experiment write-up

Data/output folders:
- `raw/`
- `processed/`
- `artifacts/`
- `outputs/` (or experiment-specific folders like `outputs_*`)

---

## Quick start (macOS)

### 1) Create environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2) Install dependencies
If you have `requirements.txt`:
```bash
pip install -r requirements.txt
```

Otherwise install typical deps:
```bash
pip install numpy pandas scikit-learn matplotlib seaborn statsmodels joblib
```

### 3) Configure experiment
Edit `config.py`:
- train/test dates
- `SAFE_MODE`
- `LONG_ONLY`
- `MIN_HOLD_BARS`
- costs and probability thresholds

### 4) Run full pipeline
```bash
python3 run_all.py
```

### 5) Optional diagnostics
```bash
python3 test.py
```

---

## Pipeline outputs

- **Model development**: `predictions.csv`, `model_meta.json`, trained model in `artifacts/`
- **Evaluation**: `evaluation_metrics.json`, `classification_report.txt`, `confusion_matrix.csv/.png`
- **Feature importance**: MDI/PFI CSVs and PNG charts
- **Backtest**: `backtest_metrics.json`, `equity_curve.csv/.png`

---

## Strategy modes

- `SAFE_MODE=True` → conservative profile
- `SAFE_MODE=False` → aggressive profile
- `LONG_ONLY=True` → no short positions (`0/+1`)
- `LONG_ONLY=False` → short allowed (`-1/0/+1`)

---

## Reproducibility notes

- Use fixed train/test windows from `config.py`
- Keep `RANDOM_STATE` fixed
- Compare runs by storing each experiment in a dedicated outputs folder (for example `outputs_Safe_Strategy_shortNotAllowed/`)

---

## Disclaimer

This project is for research/education. It is not financial advice.