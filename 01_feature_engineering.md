## 01_feature_engineering.py

In this step, we transform raw OHLCV data into model-ready features and save them to:

- `processed/features.csv`

### What we build

We compute:

- **Momentum**: `ret_1`, `ret_6`, `rsi_14`, `ret_lag1`
- **Volatility**: `vol_12`, optional `vol_spike`
- **Trend**: `ma_gap_8_24`, `ma_cross_8_24`
- **Serial correlation**: `autocorr_24_lag1`
- **Regime**: `regime_prob_high_vol`, `regime_state_high_vol`

Windows come from `mode_profile.py` via `get_mode_params()`.

### Regime logic

We estimate high-volatility regime probability using a 2-state Markov model:

- If `statsmodels` is available and data is sufficient, we fit `MarkovRegression`.
- If not, we use a rolling-volatility fallback rule.

### Notes

- We keep `close` and `market_ret_1` in the feature file for downstream evaluation/backtest steps.
- We replace inf values and keep NaNs for later cleaning in model development.