

import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance

from config import ARTIFACTS_DIR, OUTPUT_DIR, RANDOM_STATE
from utils import ensure_directories


CLUSTERS = {
    "momentum": ["ret_1", "ret_6", "rsi_14"],
    "trend": ["ma_gap_8_24", "ma_cross_8_24"],
    "volatility": ["vol_12"],
    "serial_corr": ["autocorr_24_lag1", "ret_lag1"],
    "regime": ["regime_prob_high_vol", "regime_state_high_vol"],
}


def cluster_sum(imp: pd.Series, clusters: dict) -> pd.Series:
    out = {}
    for c, feats in clusters.items():
        present = [f for f in feats if f in imp.index]
        out[c] = float(imp.loc[present].sum()) if present else 0.0
    return pd.Series(out).sort_values(ascending=False)


def save_bar(series: pd.Series, path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 4))
    series.sort_values().plot(kind="barh", ax=ax)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    ensure_directories()

    model = joblib.load(ARTIFACTS_DIR / "rf_model.pkl")
    X_test = pd.read_csv(ARTIFACTS_DIR / "X_test.csv", index_col=0)
    y_test = pd.read_csv(ARTIFACTS_DIR / "y_test.csv", index_col=0).squeeze("columns").astype(int)

    mdi = pd.Series(model.feature_importances_, index=X_test.columns).sort_values(ascending=False)
    mdi.to_csv(OUTPUT_DIR / "mdi_feature_importance.csv", header=["importance"])

    pfi_obj = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="f1_macro",
        n_repeats=10,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    pfi = pd.Series(pfi_obj.importances_mean, index=X_test.columns).sort_values(ascending=False)
    pfi.to_csv(OUTPUT_DIR / "pfi_feature_importance.csv", header=["importance"])

    mdi_cluster = cluster_sum(mdi, CLUSTERS)
    pfi_cluster = cluster_sum(pfi, CLUSTERS)

    mdi_cluster.to_csv(OUTPUT_DIR / "mdi_cluster_importance.csv", header=["importance"])
    pfi_cluster.to_csv(OUTPUT_DIR / "pfi_cluster_importance.csv", header=["importance"])

    save_bar(mdi.head(12), OUTPUT_DIR / "mdi_top_features.png", "MDI - Top Features")
    save_bar(pfi.head(12), OUTPUT_DIR / "pfi_top_features.png", "PFI - Top Features")
    save_bar(mdi_cluster, OUTPUT_DIR / "mdi_cluster_importance.png", "MDI - Cluster Importance")
    save_bar(pfi_cluster, OUTPUT_DIR / "pfi_cluster_importance.png", "PFI - Cluster Importance")

    print("[OK] Feature importance saved.")


if __name__ == "__main__":
    main()