## utils.py

This file is the shared toolbox across the pipeline.

We keep common data handling and indicator logic here so other scripts stay clean and consistent.

## What this file provides

### 1) `ensure_directories()`
Creates required folders if they do not exist:
- `processed/`
- `outputs/`
- `artifacts/`

This prevents save errors later.

### 2) `_find_col(columns, candidates)`
Matches column names flexibly:
- tries exact lowercase match first
- falls back to substring match

This helps when CSV schemas vary (for example `timestamp` vs `date`, or `adj_close` vs `close`).

### 3) `load_prices(csv_path)`
Main data normalizer. It does:

- read CSV
- detect and parse datetime column
- sort by time and set index
- remove timezone if present
- if multiple assets exist, keep the dominant symbol
- rename to standard OHLCV names (`open`, `high`, `low`, `close`, `volume`)
- coerce numeric columns
- ensure `close` exists
- fill missing `volume` with 0 when needed
- drop rows with missing `close`
- remove duplicate timestamps

Result: a clean OHLCV dataframe ready for feature engineering.

### 4) `rsi(series, window=14)`
Computes RSI with exponential smoothing:

- `delta = P_t - P_(t-1)`
- `gain = max(delta, 0)`
- `loss = max(-delta, 0)`
- `RS = EMA(gain) / (EMA(loss) + eps)`
- `RSI = 100 - 100 / (1 + RS)`

RSI stays in `[0, 100]` and captures momentum pressure.

### 5) `infer_bars_per_year(index, default=24*365)`
Infers frequency from the median timestamp delta and annualizes it:

- `bars_per_year = (365 * 24 * 3600) / median_seconds_per_bar`

If inference is unreliable, we use the default hourly value (`8760`).

This is used for annualized backtest metrics like volatility, Sharpe, Sortino, and CAGR.

## Why this file matters

Centralizing low-level data hygiene reduces duplicated logic and keeps behavior consistent across pipeline stages.

Note: `json` is currently imported but unused, so it can be removed safely.