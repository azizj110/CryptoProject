## 06_backtest_optional.py

This file converts model predictions into a trading simulation on the test period  
it is optional in pipeline order but essential if we want to answer the real question did prediction quality translate into PnL

### what goes in

- `outputs/predictions.csv`  
  (`y_pred`, optional `y_prob_up`, `market_ret_1`, `close`)
- config controls  
  `COST_BPS`, `LONG_ONLY`, thresholds, holding constraints
- mode profile controls from `mode_profile.py`  
  mainly `up_th`, `down_th`, `min_hold`, and `neutral_to_long`

### what comes out

- `outputs/backtest_metrics.json`
- `outputs/equity_curve.csv`
- `outputs/equity_curve.png`

---

### signal to position logic

we first map probabilities to raw signals

\[
s_t =
\begin{cases}
+1 & \text{if } p_t \ge \text{up\_th}\\
-1 & \text{if } p_t \le \text{down\_th}\\
0 & \text{otherwise}
\end{cases}
\]

if `LONG_ONLY=True`  
- conservative mode usually maps to \(\{1,0\}\)  
- aggressive mode can map neutral to long (stay exposed unless explicit down)

then we enforce minimum holding bars with `_apply_min_hold` so positions do not flip too often

very important  
we shift one bar before applying returns

\[
\text{position}_t = s_{t-1}
\]

this avoids lookahead bias

---

### returns and costs

strategy return per bar

\[
r^{strat}_t = \text{position}_t \cdot r^{mkt}_t - \text{cost}_t
\]

turnover is computed from position changes

\[
\text{turnover}_t = \frac{|\text{position}_t-\text{position}_{t-1}|}{2}
\]

trading cost

\[
\text{cost}_t = \text{turnover}_t \cdot \frac{\text{COST\_BPS}}{10000}
\]

buy and hold benchmark is just market return

\[
r^{bh}_t = r^{mkt}_t
\]

---

### performance metrics

equity curve

\[
E_t = \prod_{i=1}^{t}(1+r_i)
\]

reported stats include

- `FinalEquity`
- `CAGR`

\[
\text{CAGR}=E_T^{\frac{\text{bars\_per\_year}}{T}}-1
\]

- annualized volatility

\[
\sigma_{ann} = \text{std}(r)\sqrt{\text{bars\_per\_year}}
\]

- Sharpe

\[
\text{Sharpe}=\frac{\mu_{ann}}{\sigma_{ann}}
\]

- Sortino (downside volatility in denominator)
- Max Drawdown

\[
\text{MDD}=\min_t\left(\frac{E_t}{\max_{i\le t}E_i}-1\right)
\]

- average holding period in bars

---

### why this file matters

section 5 tells us if labels are predicted better than chance  
this section tells us if those predictions are tradable after costs and execution assumptions  
so this is where we compare strategy vs buy and hold on absolute return and risk adjusted return