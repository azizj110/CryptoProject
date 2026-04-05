## utils.py

This file is our shared toolbox  
we use it across all pipeline stages to keep data handling and basic indicators consistent

### what this file does

### 1) `ensure_directories()`
We create required folders if they do not exist

- `processed/`
- `outputs/`
- `artifacts/`

This avoids file-save errors in later steps

---

### 2) `_find_col(columns, candidates)`
We match column names in a flexible way

- exact lowercase match first
- fallback to substring match

This helps when input CSV naming changes like `timestamp` vs `date` or `adj_close` vs `close`

---

### 3) `load_prices(csv_path)`
This is the main data normalizer

We do the following in order

- read CSV
- detect datetime column and parse it
- sort by time and set index
- drop timezone when possible
- if multiple assets exist we keep the dominant symbol
- rename columns to standard names: `open high low close volume`
- coerce numeric columns
- ensure `close` exists (required)
- fill missing `volume` with 0 if needed
- drop rows with missing close
- remove duplicated timestamps

Result is a clean OHLCV dataframe ready for feature engineering

---

### 4) `rsi(series, window=14)`
We compute RSI using exponential smoothing

\[
\Delta_t = P_t - P_{t-1}
\]
\[
\text{gain}_t = \max(\Delta_t,0), \quad \text{loss}_t = \max(-\Delta_t,0)
\]
\[
RS_t = \frac{EMA(\text{gain})}{EMA(\text{loss})+\epsilon}
\]
\[
RSI_t = 100 - \frac{100}{1+RS_t}
\]

So RSI is bounded in \([0,100]\) and captures momentum pressure

---

### 5) `infer_bars_per_year(index, default=24*365)`
We infer data frequency from median time delta between timestamps then annualize

\[
\text{bars\_per\_year} = \frac{365 \cdot 24 \cdot 3600}{\text{median\_seconds\_per\_bar}}
\]

If inference is not reliable we fallback to default hourly frequency (`8760`)

This is used by backtest metrics for annualized volatility Sharpe Sortino and CAGR

---

### why this file matters

we keep all low-level data hygiene in one place  
that makes every stage cleaner and reduces duplicated logic

small note  
`json` import in this file is currently unused so we can remove it without changing behavior