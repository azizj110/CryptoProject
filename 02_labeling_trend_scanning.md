## 02_labeling_trend_scanning.py

This file creates the target labels for the model using trend scanning  
instead of fixed horizon labeling we scan several forward horizons and keep the one with the strongest statistical trend

output is saved to `processed/labels.csv`

### what goes in

- raw prices loaded from `prices.csv`
- close series only
- config params:
  - `MIN_TREND_H`
  - `MAX_TREND_H`
  - `TREND_STEP`
  - `T_VALUE_MIN`

### what comes out

A time indexed label table with

- `label` in `{+1, -1, 0}`
- `t_value` best trend t-stat
- `horizon` selected forward horizon
- `future_ret` realized return over selected horizon

---

### core logic

### 1) slope t-value on a window

For a candidate window \(y\) (log prices) we fit a simple linear trend

\[
y_t = \alpha + \beta x_t + \varepsilon_t
\]

with \(x_t = 0,1,2,\dots,n-1\) then centered

\[
\beta = \frac{\sum x_t y_t}{\sum x_t^2}
\]

residual variance estimate

\[
\hat{\sigma}^2 = \frac{\sum \hat{\varepsilon}_t^2}{n-2}
\]

standard error of slope

\[
SE(\beta) = \sqrt{\frac{\hat{\sigma}^2}{\sum x_t^2}}
\]

t-value

\[
t_\beta = \frac{\beta}{SE(\beta)}
\]

This is what `slope_t_value` computes  
if sample is too short or numerically unstable we return 0 for safety

### 2) trend scanning at each timestamp

For each time \(i\)

- we test horizons \(h \in [\text{min\_h}, \text{max\_h}]\)
- for each \(h\) we compute t-value on `log(close[i : i+h])`
- we select horizon \(h^*\) that maximizes \(|t|\)

\[
h^* = \arg\max_h |t_h|
\]

This gives the most statistically significant local trend around that starting point

### 3) label assignment

Using the best t-value \(t^*\)

\[
\text{label}_i =
\begin{cases}
+1 & \text{if } t^* \ge 0 \\
-1 & \text{if } t^* < 0
\end{cases}
\]

and if `abs(t*) < T_VALUE_MIN` we set label to 0 (no-trade / weak trend)

### 4) realized forward return

For selected horizon \(h^*\)

\[
\text{future\_ret}_i = \frac{P_{i+h^*}}{P_i} - 1
\]

This is saved for diagnostics and analysis not as an input feature

---

### design notes

- we use **log prices** because trend slope is more stable and scale friendly
- we use **variable horizon labels** so the label adapts to local market speed
- first/last rows may be unlabeled when forward window is not available this is expected
- this step uses future data by design but only for **target construction** not features

---

### pipeline role

This is section 2 of the project  
`labels.csv` is merged with engineered features in section 3 to train the classifier