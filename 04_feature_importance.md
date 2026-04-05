## 04_feature_importance.py

This file explains which inputs drive the model decisions  
we compute feature importance in two complementary ways then aggregate results by feature family

outputs are written to the `outputs/` folder as csv tables and plots

### what goes in

- trained model from `artifacts/rf_model.pkl`
- test features `artifacts/X_test.csv`
- test labels `artifacts/y_test.csv`

### what comes out

- `mdi_feature_importance.csv`
- `pfi_feature_importance.csv`
- `mdi_cluster_importance.csv`
- `pfi_cluster_importance.csv`
- charts:
  - `mdi_top_features.png`
  - `pfi_top_features.png`
  - `mdi_cluster_importance.png`
  - `pfi_cluster_importance.png`

---

### two importance methods

### 1) MDI (mean decrease impurity)

For tree ensembles each split reduces impurity  
MDI sums impurity decreases attributable to each feature across all trees

informally

\[
I_j^{MDI} = \sum_{\text{trees}} \sum_{\text{splits using } j} \Delta \text{impurity}
\]

then normalized by sklearn so importances sum to 1

Pros
- fast
- built in for random forest

Limitations
- can be biased toward high cardinality or correlated features

### 2) PFI (permutation feature importance)

PFI measures drop in performance when a feature is randomly shuffled  
if shuffling feature \(j\) hurts score a lot then that feature was useful

\[
I_j^{PFI} = \mathbb{E}\big[s(\hat f, X, y) - s(\hat f, \pi_j(X), y)\big]
\]

where \(s\) is macro F1 in our case and \(\pi_j(X)\) is dataset with column \(j\) permuted

Pros
- model agnostic
- directly tied to evaluation metric (`f1_macro`)

Limitations
- slower
- can dilute importance when features are highly correlated

---

### cluster level interpretation

To make interpretation cleaner we group features into families

- momentum
- trend
- volatility
- serial correlation
- regime

Then for each family we sum member importances

\[
I_{cluster} = \sum_{j \in cluster} I_j
\]

This helps answer practical questions like  
is the model driven more by momentum or by regime information

---

### implementation notes

- `cluster_sum` handles missing columns safely
- `save_bar` standardizes plotting and image export
- PFI uses `n_repeats=10` for stability vs speed tradeoff
- everything is computed on the **test feature frame** loaded from artifacts for consistency

---

### pipeline role

This is a diagnostics and interpretability step  
it does not change predictions but helps us understand why the model behaves as it does  
especially useful when discussing conservative vs aggressive behavior in the report