
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import (
    OUTPUT_DIR,
    COST_BPS,
    UP_PROBA_TH,
    DOWN_PROBA_TH,
    LONG_ONLY,
    MIN_HOLD_BARS,
)
from utils import ensure_directories, infer_bars_per_year
from mode_profile import get_mode_params


def max_drawdown(equity: pd.Series) -> float:
    dd = equity / equity.cummax() - 1.0
    return float(dd.min())


def perf_stats(returns: pd.Series, bars_per_year: int) -> dict:
    r = returns.dropna()
    if len(r) == 0:
        return {
            "CAGR": np.nan,
            "Volatility": np.nan,
            "Sharpe": np.nan,
            "Sortino": np.nan,
            "MaxDrawdown": np.nan,
            "FinalEquity": np.nan,
        }

    equity = (1.0 + r).cumprod()
    final_eq = float(equity.iloc[-1])
    cagr = final_eq ** (bars_per_year / len(r)) - 1.0
    vol = float(r.std() * np.sqrt(bars_per_year))

    ann_mean = float(r.mean() * bars_per_year)
    sharpe = ann_mean / (vol + 1e-12)

    downside = r[r < 0].std() * np.sqrt(bars_per_year)
    sortino = ann_mean / (float(downside) + 1e-12)

    return {
        "CAGR": float(cagr),
        "Volatility": vol,
        "Sharpe": float(sharpe),
        "Sortino": float(sortino),
        "MaxDrawdown": max_drawdown(equity),
        "FinalEquity": final_eq,
    }


def average_holding_period_bars(position: pd.Series) -> float:
    p = position.fillna(0).astype(int)
    active = p != 0
    if active.sum() == 0:
        return 0.0
    grp = (p != p.shift()).cumsum()
    lengths = p[active].groupby(grp[active]).size()
    return float(lengths.mean()) if len(lengths) else 0.0


def _apply_min_hold(raw_signal: np.ndarray, min_hold: int) -> np.ndarray:
    if min_hold <= 1:
        return raw_signal.astype(int)

    pos = np.zeros(len(raw_signal), dtype=int)
    current = 0
    hold_left = 0

    for i, s in enumerate(raw_signal.astype(int)):
        if hold_left > 0:
            pos[i] = current
            hold_left -= 1
            continue

        if s != current:
            current = s
            hold_left = (min_hold - 1) if current != 0 else 0

        pos[i] = current

    return pos


def main():
    ensure_directories()

    pred = pd.read_csv(OUTPUT_DIR / "predictions.csv", index_col=0, parse_dates=True)
    pred = pred.dropna(subset=["market_ret_1"]).copy()

    mode = get_mode_params()

    if "y_prob_up" in pred.columns:
        raw_signal = np.where(
            pred["y_prob_up"] >= mode["up_th"],
            1,
            np.where(pred["y_prob_up"] <= mode["down_th"], -1, 0),
        )
    else:
        raw_signal = pred["y_pred"].astype(int).values

    if LONG_ONLY:
        if mode.get("neutral_to_long", False):
            # keep exposure in uptrends; only exit on explicit down signal
            raw_signal = np.where(raw_signal == -1, 0, 1)
        else:
            raw_signal = np.where(raw_signal == 1, 1, 0)

    held_signal = _apply_min_hold(raw_signal, mode["min_hold"])
    pred["signal"] = held_signal
    pred["position"] = pd.Series(held_signal, index=pred.index).shift(1).fillna(0).astype(int)

    turnover = pred["position"].diff().abs().fillna(0) / 2.0
    trading_cost = turnover * (COST_BPS / 10000.0)

    pred["strategy_ret"] = pred["position"] * pred["market_ret_1"] - trading_cost
    pred["buyhold_ret"] = pred["market_ret_1"]

    bars_per_year = infer_bars_per_year(pred.index, default=24 * 365)

    strategy = perf_stats(pred["strategy_ret"], bars_per_year)
    strategy["AverageHoldingPeriodBars"] = average_holding_period_bars(pred["position"])
    buy_hold = perf_stats(pred["buyhold_ret"], bars_per_year)

    out = {"strategy": strategy, "buy_and_hold": buy_hold}
    with open(OUTPUT_DIR / "backtest_metrics.json", "w") as f:
        json.dump(out, f, indent=2)

    equity = pd.DataFrame(index=pred.index)
    equity["Strategy"] = (1 + pred["strategy_ret"]).cumprod()
    equity["BuyAndHold"] = (1 + pred["buyhold_ret"]).cumprod()
    equity.to_csv(OUTPUT_DIR / "equity_curve.csv")

    fig, ax = plt.subplots(figsize=(9, 4))
    equity.plot(ax=ax)
    ax.set_title("Equity Curve")
    ax.set_ylabel("Equity")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "equity_curve.png", dpi=150)
    plt.close(fig)

    print("[OK] Backtest saved.")
    print(out)


if __name__ == "__main__":
    main()