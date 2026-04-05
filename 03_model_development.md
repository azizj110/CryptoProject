## 03_model_development.py

This file trains the primary classifier and generates out of sample predictions  
we use engineered features + trend scanning labels then train a Random Forest for binary signals \(-1,+1\)

### what goes in

- `processed/features.csv`
- `processed/labels.csv`
- config settings from `config.py`
  - fixed assignment split  
    - train `2018-01-01` to `2020-12-31`
    - test `2021-01-01` to `2021-12-31`
  - training strategy (`one_time` or walk forward variants)
  - random seed and refit settings
- mode profile from `mode_profile.py` for volatility sensitivity (`vol_weight_gamma`)

### what we do

### 1) merge and clean

We join features and labels on timestamp then

- drop NaN and inf
- keep only labels in \(\{-1,+1\}\)
- sort by time
- remove non feature columns from training matrix (`label`, `close`, `market_ret_1`, diagnostics)

### 2) fixed period split (assignment compliant)

We do a strict chronological split by date

\[
\mathcal D_{train} = [2018,2020], \quad \mathcal D_{test} = [2021]
\]

This avoids leakage and follows the task exactly

### 3) model and hyperparameter tuning

Base model is `RandomForestClassifier` with class balancing  
we tune with `RandomizedSearchCV` + `TimeSeriesSplit` and optimize macro F1

\[
F1_{macro} = \frac{F1_{-1} + F1_{+1}}{2}
\]

Parameter grid includes

- `n_estimators`
- `max_depth`
- `min_samples_leaf`
- `max_features`

### 4) volatility aware sample weighting (mode dependent)

If sensitivity mode sets `vol_weight_gamma > 0`, each training row gets a weight based on volatility feature `vol_12`

robust z score

\[
z_t = \frac{v_t - \text{median}(v)}{1.4826 \cdot MAD(v) + \epsilon}
\]

weight

\[
w_t = 1 + \gamma \cdot \text{clip}(z_t, 0, 3)
\]

So high volatility rows can have more influence when desired

### 5) training strategy

- `one_time`  
  train once on 2018 to 2020 then predict all 2021
- `expanding` / `rolling`  
  walk forward refits on growing or fixed windows then predicts next block

For strict assignment interpretation `one_time` is the cleanest choice

### 6) prediction outputs

Model writes

- `outputs/predictions.csv`
  - `y_true`
  - `y_pred`
  - `y_prob_up = P(y=+1|x)`
  - `market_ret_1`, `close` (for backtest and analysis)
- artifacts
  - `artifacts/rf_model.pkl`
  - `artifacts/X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv`
- metadata
  - `outputs/model_meta.json` with periods row counts best params CV score

---

### why this design

we keep it simple and robust  
tree model handles nonlinear interactions without heavy preprocessing  
time aware CV respects order in financial series  
and the saved metadata makes every run reproducible