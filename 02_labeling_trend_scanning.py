

import numpy as np
import pandas as pd

from config import (
    RAW_DATA_PATH,
    PROCESSED_DIR,
    MIN_TREND_H,
    MAX_TREND_H,
    TREND_STEP,
    T_VALUE_MIN,
)
from utils import ensure_directories, load_prices


def slope_t_value(y: np.ndarray) -> float:
    n = len(y)
    if n < 3:
        return 0.0

    x = np.arange(n, dtype=float)
    x = x - x.mean()
    y = y - y.mean()

    sxx = np.dot(x, x)
    if sxx <= 1e-12:
        return 0.0

    beta = np.dot(x, y) / sxx
    resid = y - beta * x
    dof = n - 2
    if dof <= 0:
        return 0.0

    se_beta = np.sqrt((np.dot(resid, resid) / dof) / sxx)
    if se_beta <= 1e-12:
        return 0.0
    return beta / se_beta


def trend_scan(close: pd.Series, min_h: int, max_h: int, step: int = 1, t_min: float = 0.0) -> pd.DataFrame:
    close = close.astype(float)
    log_p = np.log(close)
    n = len(close)

    out = pd.DataFrame(
        index=close.index,
        columns=["label", "t_value", "horizon", "future_ret"],
        dtype=float,
    )

    close_values = close.values
    log_values = log_p.values

    for i in range(n):
        max_h_i = min(max_h, n - i - 1)
        if max_h_i < min_h:
            continue

        best_t = 0.0
        best_h = np.nan

        for h in range(min_h, max_h_i + 1, step):
            y = log_values[i : i + h + 1]
            t = slope_t_value(y)
            if abs(t) > abs(best_t):
                best_t = t
                best_h = h

        if np.isnan(best_h):
            continue

        label = 1 if best_t >= 0 else -1
        if abs(best_t) < t_min:
            label = 0

        j = i + int(best_h)
        future_ret = close_values[j] / close_values[i] - 1.0
        out.iloc[i] = [label, best_t, best_h, future_ret]

    out["label"] = out["label"].astype("Int64")
    return out


def main():
    ensure_directories()
    prices = load_prices(RAW_DATA_PATH)

    labels = trend_scan(
        close=prices["close"],
        min_h=MIN_TREND_H,
        max_h=MAX_TREND_H,
        step=TREND_STEP,
        t_min=T_VALUE_MIN,
    )
    labels.to_csv(PROCESSED_DIR / "labels.csv")
    print(f"[OK] Saved: {PROCESSED_DIR / 'labels.csv'}")
    print(labels["label"].value_counts(dropna=False))


if __name__ == "__main__":
    main()