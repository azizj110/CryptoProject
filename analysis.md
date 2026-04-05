# High risk high reward? Maybe
## Comparative analysis: SAFE_MODE on vs off (2021 test set)

## 1) Is this analysis coherent

Yes, globally it is coherent.

Quick consistency checks:

- both confusion matrices sum to 8760 samples (full 2021 hourly bars)
- SAFE accuracy = (2322 + 2344) / 8760 = 0.5326
- AGGR accuracy = (2383 + 2316) / 8760 = 0.5364
- interpretation aligns with backtest outputs:
  - SAFE = lower risk, lower upside
  - AGGR = higher risk, higher upside

So the analysis direction is correct.

---

## 2) Methodology check

We use a valid assignment setup:

- training strategy: `one_time`
- train: 2018-01-01 to 2020-12-31
- test: 2021-01-01 to 2021-12-31

This is clean and avoids retraining on test data.

---

## 3) Metric glossary (what each metric means)

### Classification metrics

- **Accuracy**: fraction of correct class predictions.
- **Precision (macro)**: for each class (-1, +1), how many predicted labels are correct, then average equally.
- **Recall (macro)**: for each class, how many true labels are recovered, then average equally.
- **F1 (macro)**: harmonic mean of precision and recall per class, then average equally.

Why macro: it gives equal weight to both classes, even if class frequencies differ.

### Trading metrics

- **Final Equity**: ending capital multiplier.  
  Example: 1.40 means +40% total.
- **CAGR**: annualized growth rate.
- **Volatility**: annualized standard deviation of returns.
- **Sharpe**: risk-adjusted return using total volatility.
- **Sortino**: risk-adjusted return using downside volatility only.
- **Max Drawdown**: worst peak-to-trough equity decline.
- **Average Holding Bars**: average trade duration in bars.

---

## 4) Feature glossary (what model inputs mean)

- **ret_1**: 1-bar return `(P_t / P_{t-1} - 1)`.
- **ret_6**: 6-bar return (or mode-adjusted return window).
- **rsi_14**: 14-period RSI momentum oscillator (0 to 100).
- **vol_12**: rolling return volatility over 12 bars (or mode-adjusted window).
- **ma_gap_8_24**: trend spread = `SMA_fast / SMA_slow - 1`.
- **ma_cross_8_24**: binary trend flag: fast MA above slow MA or not.
- **autocorr_24_lag1**: rolling lag-1 autocorrelation of returns.
- **ret_lag1**: previous bar return.
- **vol_spike**: normalized return shock `abs(ret_1) / vol_12` (when enabled).
- **regime_prob_high_vol**: probability of high-vol regime (Markov switching output).
- **regime_state_high_vol**: binary high-vol regime state from that probability.

Cluster names in feature-importance plots:

- **momentum**: ret_1, ret_6, rsi_14
- **trend**: ma_gap_8_24, ma_cross_8_24
- **volatility**: vol_12
- **serial_corr**: autocorr_24_lag1, ret_lag1
- **regime**: regime_prob_high_vol, regime_state_high_vol

---

## 5) Executive summary

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

Interpretation:
- SAFE mode protects capital path better.
- AGGR mode captures trends better and beats buy-and-hold in this run.
- AGGR does this with much larger absolute risk.

---

## 6) SAFE_MODE = True (conservative profile)

### Classification
- Accuracy: **0.5326**
- Macro Precision: **0.5335**
- Macro Recall: **0.5335**
- Macro F1: **0.5326**

Confusion matrix:

| True \\ Pred | -1 | +1 |
|---|---:|---:|
| -1 | 2322 | 1874 |
| +1 | 2220 | 2344 |

### Trading
- Final Equity: **1.4047**
- CAGR: **40.47%**
- Volatility: **28.51%**
- Max Drawdown: **-23.65%**

Interpretation:
- profitable but below buy-and-hold on total return
- much lower volatility and shallower drawdown

### Visuals (safe run)
![SAFE - Confusion Matrix](./outputs_Safe_Strategy/confusion_matrix.png)  
![SAFE - Equity Curve](./outputs_Safe_Strategy/equity_curve.png)  
![SAFE - MDI Top Features](./outputs_Safe_Strategy/mdi_top_features.png)  
![SAFE - MDI Cluster Importance](./outputs_Safe_Strategy/mdi_cluster_importance.png)  
![SAFE - PFI Top Features](./outputs_Safe_Strategy/pfi_top_features.png)  
![SAFE - PFI Cluster Importance](./outputs_Safe_Strategy/pfi_cluster_importance.png)

---

## 7) SAFE_MODE = False (aggressive profile)

### Classification
- Accuracy: **0.5364**
- Macro Precision: **0.5377**
- Macro Recall: **0.5377**
- Macro F1: **0.5364**

Confusion matrix:

| True \\ Pred | -1 | +1 |
|---|---:|---:|
| -1 | 2383 | 1813 |
| +1 | 2248 | 2316 |

### Trading
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
- better upside capture and final return than benchmark
- still very high-risk profile in absolute terms

### Visuals (aggressive run)
![AGGR - Confusion Matrix](./outputs_Agressive_Strategy/confusion_matrix.png)  
![AGGR - Equity Curve](./outputs_Agressive_Strategy/equity_curve.png)  
![AGGR - MDI Top Features](./outputs_Agressive_Strategy/mdi_top_features.png)  
![AGGR - MDI Cluster Importance](./outputs_Agressive_Strategy/mdi_cluster_importance.png)  
![AGGR - PFI Top Features](./outputs_Agressive_Strategy/pfi_top_features.png)  
![AGGR - PFI Cluster Importance](./outputs_Agressive_Strategy/pfi_cluster_importance.png)

---

## 8) Delta analysis (SAFE off minus SAFE on)

- Accuracy: **+0.0038**
- Macro F1: **+0.0037**
- Final Equity: **+0.2779**
- CAGR: **+27.79 pp**
- Volatility: **+61.78 pp**
- Max Drawdown: **-26.58 pp** (deeper drawdown)
- Avg Holding: **+32.29 bars**

Interpretation:
- turning SAFE off increases trend participation and return
- cost is much larger risk and drawdown depth

---

## 9) Final answer

Is this high risk high reward

- SAFE mode: mostly **no** (defensive profile)
- SAFE off: mostly **yes** (aggressive profile)

---

## 10) Practical recommendation

- Use `SAFE_MODE = True` if stability and capital protection are primary.
- Use `SAFE_MODE = False` if maximizing upside is primary and deep drawdowns are acceptable.
- Best next step: add regime-switch logic to toggle between profiles dynamically.