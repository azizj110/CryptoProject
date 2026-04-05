## 01_feature_engineering.py

This file builds the model input features from raw price data  
output is `processed/features.csv`

### main logic

we compute returns momentum volatility trend serial correlation and regime features

- one bar return  
  `r_t = P_t / P_(t-1) - 1`
- k bar return  
  `r_t(k) = P_t / P_(t-k) - 1`
- rolling volatility  
  `vol_t = std(r_(t-w+1) ... r_t)`
- moving average gap  
  `ma_gap_t = SMA_fast_t / SMA_slow_t - 1`
- crossover flag  
  `ma_cross_t = 1 if SMA_fast_t > SMA_slow_t else 0`
- lag feature  
  `ret_lag1_t = r_(t-1)`

we also compute RSI and optional `vol_spike` when aggressive mode is enabled

### regime model

we use a 2-state Markov switching model on returns

`r_t = mu_(S_t) + epsilon_t`  
`epsilon_t ~ N(0, sigma_(S_t)^2)`

then we store

- `regime_prob_high_vol`
- `regime_state_high_vol`

if statsmodels is unavailable we fallback to a rolling-vol rule based regime proxy

### notes

this file also keeps `close` and `market_ret_1` for later evaluation and backtest