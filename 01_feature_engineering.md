## 01_feature_engineering.py

This script turns raw price data into model-ready features.

**Output**
- `processed/features.csv`

## What we build

We create feature groups for:
- momentum
- volatility
- trend
- serial correlation
- market regime

Main examples:
- `ret_1 = close / close.shift(1) - 1`
- `ret_k = close / close.shift(k) - 1`
- rolling volatility from `ret_1` over window `w`
- `ma_gap = sma_fast / sma_slow - 1`
- `ma_cross = 1` when `sma_fast > sma_slow`, else `0`
- `ret_lag1 = ret_1.shift(1)`

We also add:
- RSI
- optional `vol_spike` (enabled in aggressive mode)

## Regime detection

We try a 2-state Markov switching model on returns and store:
- `regime_prob_high_vol`
- `regime_state_high_vol`

If `statsmodels` is unavailable, we fall back to a rolling-volatility rule.

## Important note

We keep:
- `close`
- `market_ret_1`

These columns are needed later for evaluation and backtesting.