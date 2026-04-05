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


def _signal_from_proba(prob_up: pd.Series, mode: dict, long_only: bool) -> pd.Series:
    p = (
        prob_up.astype(float)
        .clip(lower=0.0, upper=1.0)
        .ewm(span=int(mode.get("prob_ewm_span", 12)), adjust=False)
        .mean()
    )

    entry_long = float(mode.get("entry_long", mode.get("up_th", 0.55)))
    exit_long = float(mode.get("exit_long", 0.50))
    entry_short = float(mode.get("entry_short", mode.get("down_th", 0.45)))
    exit_short = float(mode.get("exit_short", 0.50))
    confirm = max(1, int(mode.get("confirm_bars", 1)))
    allow_flip = bool(mode.get("allow_direct_flip", False))

    out = np.zeros(len(p), dtype=int)
    pos = 0
    up_run = 0
    down_run = 0

    for i, x in enumerate(p.to_numpy()):
        up_run = up_run + 1 if x >= entry_long else 0
        down_run = down_run + 1 if x <= entry_short else 0

        if pos == 1:
            if x <= exit_long:
                pos = 0
            if allow_flip and (not long_only) and down_run >= confirm:
                pos = -1

        elif pos == -1:
            if x >= exit_short:
                pos = 0
            if allow_flip and up_run >= confirm:
                pos = 1

        else:
            if up_run >= confirm:
                pos = 1
            elif (not long_only) and down_run >= confirm:
                pos = -1

        if long_only and pos == -1:
            pos = 0

        out[i] = pos

    sig = pd.Series(out, index=prob_up.index, dtype=int, name="signal")
    if long_only and mode.get("neutral_to_long", False):
        sig = sig.replace(0, 1)
    return sig


def main():
    ensure_directories()

    pred = pd.read_csv(OUTPUT_DIR / "predictions.csv", index_col=0, parse_dates=True)
    pred = pred.dropna(subset=["market_ret_1"]).copy()

    mode = get_mode_params()

    if "y_prob_up" in pred.columns:
        signal = _signal_from_proba(pred["y_prob_up"], mode, LONG_ONLY)
    else:
        signal = pred["y_pred"].astype(int).copy()
        if LONG_ONLY:
            signal = signal.clip(lower=0)
            if mode.get("neutral_to_long", False):
                signal = signal.replace(0, 1)

    hold_bars = max(int(MIN_HOLD_BARS), int(mode.get("min_hold", MIN_HOLD_BARS)))
    signal = _apply_min_hold(signal, hold_bars)
    pred["signal"] = signal
    pred["position"] = pd.Series(signal, index=pred.index).shift(1).fillna(0).astype(int)

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