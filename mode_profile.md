## mode_profile.py

This file is the behavior switch of the strategy  
we use it to keep one pipeline but run it in two personalities conservative vs volatility sensitive

it reads base settings from `config.py` and returns a single dictionary through `get_mode_params()`  
other files consume this dictionary

- `01_feature_engineering.py` for feature windows and `vol_spike`
- `03_model_development.py` for volatility sample weighting
- `06_backtest_optional.py` for thresholds hold logic and neutral handling

---

### mode logic

we branch on `SAFE_MODE`

### 1) `SAFE_MODE = True` (conservative)

we slow the system down and reduce noise chasing

- longer windows  
  `ret_window=6`, `vol_window=12`, `sma 8/24`, `autocorr 24`
- stricter thresholds  
  \[
  up\_th = \max(UP\_PROBA\_TH,\ 0.60)
  \]
  \[
  down\_th = \min(DOWN\_PROBA\_TH,\ 0.40)
  \]
- longer minimum hold  
  \[
  min\_hold = \max(MIN\_HOLD\_BARS,\ 6)
  \]
- no extra volatility feature pressure  
  `enable_vol_spike=False`, `vol_weight_gamma=0.0`
- neutral stays neutral  
  `neutral_to_long=False`

### 2) `SAFE_MODE = False` (aggressive / volatility sensitive)

we make the system react faster to variation and trends

- shorter windows  
  `ret_window=3`, `vol_window=8`, `sma 6/18`, `autocorr 12`
- more permissive thresholds  
  \[
  up\_th = \min(0.55,\ UP\_PROBA\_TH - 0.05)
  \]
  \[
  down\_th = \max(0.45,\ DOWN\_PROBA\_TH + 0.05)
  \]
- shorter holding constraint  
  \[
  min\_hold = \min\left(3,\ \max(1,\lfloor MIN\_HOLD\_BARS/2 \rfloor)\right)
  \]
- volatility sensitivity enabled  
  `enable_vol_spike=True`, `vol_weight_gamma=0.6`
- neutral can stay long  
  `neutral_to_long=True`

---

### why this file matters

we separate policy from mechanics  
mechanics stay in training and backtest files while this file defines risk posture  
that makes experiments cleaner because we can flip one boolean and compare behavior under the same data and model family