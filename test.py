import numpy as np
import pandas as pd

from config import OUTPUT_DIR, LONG_ONLY, MIN_HOLD_BARS
from mode_profile import get_mode_params

m = get_mode_params()
p = pd.read_csv(OUTPUT_DIR / "predictions.csv", index_col=0, parse_dates=True)

def signal_from_proba(prob_up: pd.Series, mode: dict, long_only: bool) -> pd.Series:
    p_sm = (
        prob_up.astype(float)
        .clip(0.0, 1.0)
        .ewm(span=int(mode.get("prob_ewm_span", 12)), adjust=False)
        .mean()
    )

    entry_long = float(mode.get("entry_long", mode.get("up_th", 0.55)))
    exit_long = float(mode.get("exit_long", 0.50))
    entry_short = float(mode.get("entry_short", mode.get("down_th", 0.45)))
    exit_short = float(mode.get("exit_short", 0.50))
    confirm = max(1, int(mode.get("confirm_bars", 1)))
    allow_flip = bool(mode.get("allow_direct_flip", False))

    out = np.zeros(len(p_sm), dtype=int)
    pos = 0
    up_run = 0
    down_run = 0

    for i, x in enumerate(p_sm.to_numpy()):
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

def apply_min_hold(signal: pd.Series, hold_bars: int) -> pd.Series:
    if hold_bars <= 1:
        return signal.astype(int)

    s = signal.astype(int).to_numpy()
    out = s.copy()
    last = out[0]
    hold = 1

    for i in range(1, len(out)):
        if out[i] != last and hold < hold_bars:
            out[i] = last
            hold += 1
        else:
            if out[i] != last:
                last = out[i]
                hold = 1
            else:
                hold += 1

    return pd.Series(out, index=signal.index, dtype=int)

if "y_prob_up" in p.columns:
    sig = signal_from_proba(p["y_prob_up"], m, LONG_ONLY)
else:
    sig = p["y_pred"].astype(int).copy()
    if LONG_ONLY:
        sig = sig.clip(lower=0)
        if m.get("neutral_to_long", False):
            sig = sig.replace(0, 1)

sig = apply_min_hold(sig, max(int(MIN_HOLD_BARS), int(m.get("min_hold", MIN_HOLD_BARS))))
pos = sig.shift(1).fillna(0).astype(int)  # traded position

print("Raw signal distribution:")
print(sig.value_counts(normalize=True).sort_index())

print("\nTraded position distribution:")
print(pos.value_counts(normalize=True).sort_index())

print("\nExposure:")
print("Long:", (pos == 1).mean())
print("Short:", (pos == -1).mean())
print("Flat:", (pos == 0).mean())