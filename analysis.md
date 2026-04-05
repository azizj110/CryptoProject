# Comparative Analysis of Strategy Configurations (2021 Test Set)

## Intro

We evaluate four configurations under the same assignment-compliant framework:

- **Train:** 2018-01-01 to 2020-12-31  
- **Test:** 2021-01-01 to 2021-12-31  
- **Training strategy:** `one_time`  
- **Model family:** Random Forest classifier + rule-based signal mapping/backtest layer  

Configurations compared:

1. **SAFE mode + short allowed**
2. **SAFE mode + short not allowed**
3. **Aggressive mode + short allowed**
4. **Aggressive mode + short not allowed**

---

## Terms used in this report

- **Accuracy**: fraction of correctly predicted labels.
- **Precision (macro)**: precision averaged equally across classes (`-1`, `+1`).
- **Recall (macro)**: recall averaged equally across classes.
- **F1 (macro)**: harmonic mean of precision/recall, averaged equally across classes.
- **Confusion matrix**: counts of true vs predicted classes.
- **CAGR**: compounded annual growth rate.
- **Volatility**: annualized standard deviation of returns.
- **Sharpe**: return per unit of total volatility.
- **Sortino**: return per unit of downside volatility.
- **Max Drawdown (MDD)**: worst peak-to-trough decline.
- **Final Equity**: ending equity multiple (starting at 1.0).
- **AverageHoldingPeriodBars**: average duration of positions.
- **MDI importance**: model impurity-based feature importance (in-model).
- **PFI importance**: permutation feature importance (out-of-sample utility).
- **Short allowed**: positions can be `-1, 0, +1`.
- **Short not allowed**: positions restricted to `0, +1` (long-only).

---

# 1) SAFE strategy

## 1.1 SAFE + short allowed

### Classification
- Accuracy: **0.5306**
- Precision (macro): **0.5305**
- Recall (macro): **0.5305**
- F1 (macro): **0.5303**

Confusion matrix:
- True -1: Pred -1 = 2217, Pred +1 = 1979
- True +1: Pred -1 = 2133, Pred +1 = 2431

![SAFE + short allowed — Confusion Matrix](outputs_Safe_Strategy_shortAllowed/confusion_matrix.png)

### Backtest
**Strategy**
- Final Equity: **0.9604**
- CAGR: **-0.0396**
- Volatility: **0.8205**
- Sharpe: **0.3669**
- Sortino: **0.3638**
- Max Drawdown: **-0.6098**
- Avg holding: **22.67 bars**

**Buy & Hold**
- Final Equity: **1.5968**
- CAGR: **0.5968**
- Volatility: **0.9414**
- Sharpe: **0.9719**
- Sortino: **1.2191**
- Max Drawdown: **-0.5476**

![SAFE + short allowed — Equity Curve](outputs_Safe_Strategy_shortAllowed/equity_curve.png)

### Feature importance (SAFE model)
- **MDI top features:** `vol_12` (0.1883), `ma_gap_8_24` (0.1686)
- **MDI top clusters:** momentum (0.3571), serial_corr (0.2443)
- **PFI top features:** `ret_6` (0.01357), `ma_gap_8_24` (0.01297)
- **PFI top clusters:** momentum (0.02006), trend (0.01398)

![SAFE + short allowed — MDI Top Features](outputs_Safe_Strategy_shortAllowed/mdi_top_features.png)
![SAFE + short allowed — MDI Cluster Importance](outputs_Safe_Strategy_shortAllowed/mdi_cluster_importance.png)
![SAFE + short allowed — PFI Top Features](outputs_Safe_Strategy_shortAllowed/pfi_top_features.png)
![SAFE + short allowed — PFI Cluster Importance](outputs_Safe_Strategy_shortAllowed/pfi_cluster_importance.png)

---

## 1.2 SAFE + short not allowed (long-only)

### Classification
(Same model quality as SAFE short-allowed run)
- Accuracy: **0.5306**
- Precision (macro): **0.5305**
- Recall (macro): **0.5305**
- F1 (macro): **0.5303**

Confusion matrix:
- True -1: Pred -1 = 2217, Pred +1 = 1979
- True +1: Pred -1 = 2133, Pred +1 = 2431

![SAFE + short not allowed — Confusion Matrix](outputs_Safe_Strategy_shortNotAllowed/confusion_matrix.png)

### Backtest
**Strategy**
- Final Equity: **1.1533**
- CAGR: **0.1533**
- Volatility: **0.1285**
- Sharpe: **1.1744**
- Sortino: **0.2243**
- Max Drawdown: **-0.1325**
- Avg holding: **20.22 bars**

**Buy & Hold**
- Final Equity: **1.5968**
- CAGR: **0.5968**
- Volatility: **0.9414**
- Sharpe: **0.9719**
- Sortino: **1.2191**
- Max Drawdown: **-0.5476**

![SAFE + short not allowed — Equity Curve](outputs_Safe_Strategy_shortNotAllowed/equity_curve.png)

### Feature importance
Same as SAFE short-allowed (same trained model and feature files).

![SAFE + short not allowed — MDI Top Features](outputs_Safe_Strategy_shortNotAllowed/mdi_top_features.png)
![SAFE + short not allowed — MDI Cluster Importance](outputs_Safe_Strategy_shortNotAllowed/mdi_cluster_importance.png)
![SAFE + short not allowed — PFI Top Features](outputs_Safe_Strategy_shortNotAllowed/pfi_top_features.png)
![SAFE + short not allowed — PFI Cluster Importance](outputs_Safe_Strategy_shortNotAllowed/pfi_cluster_importance.png)

---

## 1.3 SAFE comparison (short allowed vs short not allowed)

- Classification is essentially identical (same model quality).
- Difference is from **signal-to-position mapping**, not prediction quality.
- Disabling shorts improved outcomes materially:
  - Final Equity: **0.9604 → 1.1533**
  - MDD: **-0.6098 → -0.1325**
  - Volatility: **0.8205 → 0.1285**

**Why:**  
In this 2021 regime, the SAFE mapping with shorting likely converted modest model errors into costly short exposure and deeper drawdowns. Long-only SAFE behaves as a defensive, low-volatility filter instead.

---

# 2) Aggressive strategy

## 2.1 Aggressive + short allowed

### Classification
- Accuracy: **0.5309**
- Precision (macro): **0.5329**
- Recall (macro): **0.5327**
- F1 (macro): **0.5308**

Confusion matrix:
- True -1: Pred -1 = 2411, Pred +1 = 1785
- True +1: Pred -1 = 2324, Pred +1 = 2240

![Aggressive + short allowed — Confusion Matrix](outputs_Agressive_Strategy_shortAllowed/confusion_matrix.png)

### Backtest
**Strategy**
- Final Equity: **2.0127**
- CAGR: **1.0127**
- Volatility: **0.6174**
- Sharpe: **1.4467**
- Sortino: **0.9825**
- Max Drawdown: **-0.3230**
- Avg holding: **19.50 bars**

**Buy & Hold**
- Final Equity: **1.5968**
- CAGR: **0.5968**
- Volatility: **0.9414**
- Sharpe: **0.9719**
- Sortino: **1.2191**
- Max Drawdown: **-0.5476**

![Aggressive + short allowed — Equity Curve](outputs_Agressive_Strategy_shortAllowed/equity_curve.png)

### Exposure (reported diagnostics)
- Approx. long: **15.6%**
- Approx. short: **10.5%**
- Approx. flat: **73.9%**

### Feature importance (Aggressive model)
- **MDI top features:** `vol_12` (0.1689), `rsi_14` (0.1517)
- **MDI top clusters:** momentum (0.3574), serial_corr (0.2123)
- **PFI top feature:** `rsi_14` (0.00901)
- **PFI top clusters:** momentum (0.00909), serial_corr (0.00117)

![Aggressive + short allowed — MDI Top Features](outputs_Agressive_Strategy_shortAllowed/mdi_top_features.png)
![Aggressive + short allowed — MDI Cluster Importance](outputs_Agressive_Strategy_shortAllowed/mdi_cluster_importance.png)
![Aggressive + short allowed — PFI Top Features](outputs_Agressive_Strategy_shortAllowed/pfi_top_features.png)
![Aggressive + short allowed — PFI Cluster Importance](outputs_Agressive_Strategy_shortAllowed/pfi_cluster_importance.png)

---

## 2.2 Aggressive + short not allowed (long-only)

### Classification
(Same model quality as aggressive short-allowed run)
- Accuracy: **0.5309**
- Precision (macro): **0.5329**
- Recall (macro): **0.5327**
- F1 (macro): **0.5308**

Confusion matrix:
- True -1: Pred -1 = 2411, Pred +1 = 1785
- True +1: Pred -1 = 2324, Pred +1 = 2240

![Aggressive + short not allowed — Confusion Matrix](outputs_Agressive_Strategy_shortNotAllowed/confusion_matrix.png)

### Backtest
**Strategy**
- Final Equity: **2.2602**
- CAGR: **1.2602**
- Volatility: **0.5461**
- Sharpe: **1.7717**
- Sortino: **0.8826**
- Max Drawdown: **-0.3410**
- Avg holding: **18.76 bars**

**Buy & Hold**
- Final Equity: **1.5968**
- CAGR: **0.5968**
- Volatility: **0.9414**
- Sharpe: **0.9719**
- Sortino: **1.2191**
- Max Drawdown: **-0.5476**

![Aggressive + short not allowed — Equity Curve](outputs_Agressive_Strategy_shortNotAllowed/equity_curve.png)

### Exposure (reported diagnostics)
- long: **17.93%**
- short: **0%**
- flat: **82.07%**

### Feature importance
Same as aggressive short-allowed (same trained model and feature files).

![Aggressive + short not allowed — MDI Top Features](outputs_Agressive_Strategy_shortNotAllowed/mdi_top_features.png)
![Aggressive + short not allowed — MDI Cluster Importance](outputs_Agressive_Strategy_shortNotAllowed/mdi_cluster_importance.png)
![Aggressive + short not allowed — PFI Top Features](outputs_Agressive_Strategy_shortNotAllowed/pfi_top_features.png)
![Aggressive + short not allowed — PFI Cluster Importance](outputs_Agressive_Strategy_shortNotAllowed/pfi_cluster_importance.png)

---

## 2.3 Aggressive comparison (short allowed vs short not allowed)

- Classification remains the same; backtest mapping drives performance difference.
- In this test window, **aggressive long-only outperformed aggressive short-enabled**:
  - Final Equity: **2.2602 vs 2.0127**
  - Sharpe: **1.7717 vs 1.4467**
  - Volatility: **0.5461 vs 0.6174**

**Why:**  
In a predominantly upward market structure, short trades can reduce upside capture and add wrong-way losses. Aggressive long-only retained strong timing benefits while avoiding short-side drag.

---

# Final conclusion

Across all four runs:

1. **Model classification edge is modest (~53% macro metrics) in every case.**
2. **Performance differences come mainly from trading rules (short policy + signal mapping), not from major model-quality changes.**
3. **Best overall result in this dataset:**  
   **Aggressive + short not allowed** (highest equity and Sharpe among tested variants).
4. **Worst result:**  
   **SAFE + short allowed** (negative CAGR, largest drawdown among strategy variants).
5. **Feature importance is stable across runs:**  
   momentum/serial-correlation and selected trend features carry most useful signal; volatility feature `vol_12` is structurally important in MDI.

Practical takeaway: for this 2021 test set, **shorting should be used very selectively (or disabled)**, while aggressive long-only mapping gave the strongest risk-adjusted outcome.