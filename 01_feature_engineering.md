## 01_feature_engineering.py

This file builds the feature table we use for training and testing  
we start from raw OHLCV data and transform it into a compact set of technical and regime features  
the output is saved to `processed/features.csv`

### what goes in

- input file: `prices.csv` (loaded through `load_prices`)
- required column: `close`
- helper config:
  - data paths from `config.py`
  - mode parameters from `mode_profile.py` (safe vs more sensitive setup)

### what comes out

A dataframe indexed by time with these columns:

- `ret_1`
- `ret_6` (window from mode profile)
- `vol_12` (window from mode profile)
- `rsi_14`
- `ma_gap_8_24` (fast/slow windows from mode profile)
- `ma_cross_8_24`
- `autocorr_24_lag1` (window from mode profile)
- `ret_lag1`
- `vol_spike` (enabled only in sensitive mode)
- `regime_prob_high_vol`
- `regime_state_high_vol`
- plus passthrough columns for later stages:
  - `close`
  - `market_ret_1`

---

### core math logic

#### 1) returns and momentum
We compute simple returns as

\[
r_t = \frac{P_t}{P_{t-1}} - 1
\]

and multi period return

\[
r^{(k)}_t = \frac{P_t}{P_{t-k}} - 1
\]

where \(k\) is mode dependent (`ret_window`)

#### 2) rolling volatility
Volatility feature is rolling std of 1 bar returns

\[
\sigma_t = \text{std}(r_{t-w+1}, \dots, r_t)
\]

with \(w = \text{vol_window}\)

#### 3) RSI
RSI(14) is computed from up/down moves using the helper in `utils.py`  
it gives a bounded momentum oscillator in \([0,100]\)

#### 4) trend via moving averages
Fast and slow moving averages are built then combined into

\[
\text{ma\_gap}_t = \frac{\text{SMA}^{fast}_t}{\text{SMA}^{slow}_t} - 1
\]

and a crossover flag

\[
\text{ma\_cross}_t =
\begin{cases}
1 & \text{if } \text{SMA}^{fast}_t > \text{SMA}^{slow}_t \\
0 & \text{otherwise}
\end{cases}
\]

#### 5) serial dependence
Lag-1 rolling autocorrelation of returns

\[
\rho_t = \text{corr}(r_{t-w+1:t},\ r_{t-w:t-1})
\]

plus a direct lag feature `ret_lag1 = r_{t-1}`

#### 6) optional volatility spike feature
When sensitivity mode enables it we add

\[
\text{vol\_spike}_t = \frac{|r_t|}{\sigma_t + \varepsilon}
\]

clipped to \([0,10]\)  
this helps the model react to sudden variation bursts

---

### latent regime model (time-series appropriate)

Instead of clustering independent points we use a 2-state Markov switching model on returns:

\[
r_t = \mu_{S_t} + \epsilon_t,\quad
\epsilon_t \sim \mathcal{N}(0,\sigma^2_{S_t}),\quad
S_t \in \{0,1\}
\]

with switching variance enabled

#### procedure we use

1. fit model on an initial training chunk (`train_ratio=0.7`)
2. get filtered state probabilities on that chunk
3. identify which state is high-vol by comparing empirical variance of returns per inferred state
4. filter full sample using learned parameters
5. output:
   - `regime_prob_high_vol = P(S_t = high_vol | data_{1:t})`
   - `regime_state_high_vol = 1[prob >= 0.5]`

This gives a regime signal that respects temporal structure

---

### robustness / fallback path

If `statsmodels` is missing or data is too short, we fallback to a simple rule:

- realized vol: 24-bar std
- baseline: rolling median of realized vol over 10 days
- high-vol regime flag:

\[
\text{regime}_t = 1[\text{rv}_t > \text{baseline}_t]
\]

This keeps the pipeline stable even without Markov fitting

---

### pipeline role

This is section 1 of the full workflow  
all downstream steps depend on this output:

- section 2 labeling joins on same datetime index
- section 3 model trains on these features
- section 4 computes feature importance from trained model
- section 6 backtest uses saved `close` and `market_ret_1`