

import json
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
)

from config import OUTPUT_DIR
from utils import ensure_directories


def main():
    ensure_directories()

    pred = pd.read_csv(OUTPUT_DIR / "predictions.csv", index_col=0, parse_dates=True)
    y_true = pred["y_true"].astype(int)
    y_pred = pred["y_pred"].astype(int)

    cm = confusion_matrix(y_true, y_pred, labels=[-1, 1])

    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_macro": float(precision_score(y_true, y_pred, average="macro", zero_division=0)),
        "recall_macro": float(recall_score(y_true, y_pred, average="macro", zero_division=0)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "confusion_matrix": cm.tolist(),
    }

    with open(OUTPUT_DIR / "evaluation_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    report = classification_report(
        y_true,
        y_pred,
        labels=[-1, 1],
        target_names=["Down (-1)", "Up (+1)"],
        zero_division=0,
    )
    with open(OUTPUT_DIR / "classification_report.txt", "w") as f:
        f.write(report)

    cm_df = pd.DataFrame(cm, index=["True -1", "True +1"], columns=["Pred -1", "Pred +1"])
    cm_df.to_csv(OUTPUT_DIR / "confusion_matrix.csv")

    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["-1", "+1"])
    disp.plot(ax=ax, cmap="Blues", values_format="d", colorbar=False)
    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=150)
    plt.close(fig)

    print("[OK] Evaluation saved.")
    print(metrics)


if __name__ == "__main__":
    main()