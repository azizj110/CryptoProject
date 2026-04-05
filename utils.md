## utils.py

This module contains shared helpers used across the pipeline.

### 1) `ensure_directories()`

Creates required folders if missing:

- `processed/`
- `outputs/`
- `artifacts/`

### 2) `_find_col(columns, candidates)`

Flexible column matching:

- exact lowercase match first
- substring fallback next

### 3) `load_prices(csv_path)`

Standardizes raw data:

- parses datetime index
- sorts by time
- strips timezone where possible
- selects dominant symbol if multiple assets exist
- normalizes OHLCV names
- enforces numeric fields
- guarantees `close` exists
- fills missing `volume` with `0`
- drops duplicate timestamps

### 4) `rsi(series, window=14)`

Computes RSI via exponentially smoothed gains/losses.

### 5) `infer_bars_per_year(index, default=24*365)`

Infers frequency from median timestamp delta and returns annualized bars-per-year.
Used for annualized metrics in backtesting.

---

We keep these utilities centralized so every stage uses the same data hygiene rules.