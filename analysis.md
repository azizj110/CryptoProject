# High risk high reward? Maybe
## Comparative analysis: SAFE_MODE on vs off (2021 test set)

## 1) Methodology check

We keep a valid evaluation setup:

- training strategy: `one_time`
- train window: 2018-01-01 to 2020-12-31
- test window: 2021-01-01 to 2021-12-31

So this remains assignment-compliant and avoids walk-forward refit leakage.

---

## 2) Executive summary

| Metric | SAFE_MODE = True | SAFE_MODE = False |
|---|---:|---:|
| Accuracy | 0.5326 | 0.5364 |
| Macro F1 | 0.5326 | 0.5364 |
| Final Equity | 1.4047 | 1.6826 |
| CAGR | 40.47% | 68.26% |
| Volatility | 28.51% | 90.28% |
| Sharpe | 1.334 | 1.032 |
| Sortino | 0.501 | 1.264 |
| Max Drawdown | -23.65% | -50.23% |
| Avg Holding (bars) | 6.93 | 39.21 |
| Buy&Hold Final Equity | 1.5968 | 1.5968 |

Main conclusion:
- SAFE mode = defensive profile (lower risk, lower upside)
- SAFE off = aggressive profile (higher risk, higher upside), and in this run it beats buy-and-hold

---

## 3) SAFE_MODE = True (conservative profile)

### 3.1 Classification quality
- Accuracy: **0.5326**
- Macro Precision: **0.5335**
- Macro Recall: **0.5335**
- Macro F1: **0.5326**

Confusion matrix:

| True \\ Pred | -1 | +1 |
|---|---:|---:|
| -1 | 2322 | 1874 |
| +1 | 2220 | 2344 |

Interpretation:
- We have a small but consistent edge over random.
- Errors are fairly balanced across classes.

### 3.2 Trading quality
- Final Equity: **1.4047** (profitable in absolute terms)
- CAGR: **40.47%**
- Volatility: **28.51%**
- Max Drawdown: **-23.65%**

Interpretation:
- Strong downside control and smoother path.
- Underperforms buy-and-hold on total return in 2021.

### 3.3 Feature behavior
- Prior safe run was mostly trend/momentum driven.
- `ma_gap_8_24` remained a core signal in that regime.

### 3.4 Visuals (safe run)
![SAFE - Confusion Matrix](./outputs_safe/confusion_matrix.png)  
![SAFE - Equity Curve](./outputs_safe/equity_curve.png)  
![SAFE - MDI Top Features](./outputs_safe/mdi_top_features.png)  
![SAFE - MDI Cluster Importance](./outputs_safe/mdi_cluster_importance.png)  
![SAFE - PFI Top Features](./outputs_safe/pfi_top_features.png)  
![SAFE - PFI Cluster Importance](./outputs_safe/pfi_cluster_importance.png)

---

## 4) SAFE_MODE = False (aggressive profile)

### 4.1 Classification quality
- Accuracy: **0.5364**
- Macro Precision: **0.5377**
- Macro Recall: **0.5377**
- Macro F1: **0.5364**

Confusion matrix:

| True \\ Pred | -1 | +1 |
|---|---:|---:|
| -1 | 2383 | 1813 |
| +1 | 2248 | 2316 |

Interpretation:
- Small but measurable improvement vs safe mode.
- Class behavior remains balanced.

### 4.2 Trading quality
- Final Equity: **1.6826**
- CAGR: **68.26%**
- Volatility: **90.28%**
- Sharpe: **1.032**
- Sortino: **1.264**
- Max Drawdown: **-50.23%**

Benchmark (buy-and-hold):
- Final Equity: **1.5968**
- CAGR: **59.68%**
- Volatility: **94.14%**
- Sharpe: **0.972**
- Sortino: **1.219**
- Max Drawdown: **-54.76%**

Interpretation:
- We outperform buy-and-hold on return and slightly on risk-adjusted metrics in this run.
- Risk remains high in absolute terms (large swings, deep drawdowns).

### 4.3 Feature behavior
- Top feature is clearly **`rsi_14`**.
- `ma_gap_8_24` remains important.
- Momentum dominates cluster importance, especially in PFI.

### 4.4 Visuals (aggressive run)
![AGGR - Confusion Matrix](./outputs_aggressive/confusion_matrix.png)  
![AGGR - Equity Curve](./outputs_aggressive/equity_curve.png)  
![AGGR - MDI Top Features](./outputs_aggressive/mdi_top_features.png)  
![AGGR - MDI Cluster Importance](./outputs_aggressive/mdi_cluster_importance.png)  
![AGGR - PFI Top Features](./outputs_aggressive/pfi_top_features.png)  
![AGGR - PFI Cluster Importance](./outputs_aggressive/pfi_cluster_importance.png)

---

## 5) Delta analysis (SAFE off minus SAFE on)

- Accuracy: **+0.0038**
- Macro F1: **+0.0037**
- Final Equity: **+0.2779**
- CAGR: **+27.79 pp**
- Volatility: **+61.78 pp**
- Max Drawdown: **-26.58 pp** (deeper drawdown)
- Avg Holding: **+32.29 bars**

Interpretation:
- Turning safe mode off increases trend capture and total return.
- Cost is materially higher risk and larger drawdown exposure.

---

## 6) Final answer to title question

Is this high risk high reward maybe

- For SAFE mode: **no**, it is mostly lower-risk/moderate-reward.
- For SAFE off: **yes mostly**, this behaves like high-risk/high-reward and beat buy-and-hold in this 2021 run.

---

## 7) Practical recommendation

- Use **SAFE_MODE = True** when capital protection and smoother equity path are the priority.
- Use **SAFE_MODE = False** when we accept higher drawdown to maximize upside capture.
- For production use, we should add regime-based switching between the two profiles instead of keeping one fixed all year.