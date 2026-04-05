from config import SAFE_MODE, UP_PROBA_TH, DOWN_PROBA_TH, MIN_HOLD_BARS

def get_mode_params():
    if SAFE_MODE:
        # Conservative profile
        return {
            "profile": "conservative",
            "ret_window": 8,
            "vol_window": 16,
            "sma_fast": 10,
            "sma_slow": 30,
            "autocorr_window": 24,

            # less passive thresholds
            "entry_long": 0.54,
            "exit_long": 0.50,
            "entry_short": 0.46,
            "exit_short": 0.50,

            "prob_ewm_span": 10,
            "confirm_bars": 1,
            "allow_direct_flip": False,

            "min_hold": 3,
            "enable_vol_spike": False,
            "vol_weight_gamma": 0.0,
            "neutral_to_long": False,
        }

    # Aggressive profile
    entry_long = min(0.56, max(0.51, UP_PROBA_TH - 0.04))
    entry_short = max(0.44, min(0.49, DOWN_PROBA_TH + 0.04))
    return {
        "profile": "aggressive",
        "ret_window": 4,
        "vol_window": 10,
        "sma_fast": 6,
        "sma_slow": 18,
        "autocorr_window": 12,

        "up_th": entry_long,
        "down_th": entry_short,
        "entry_long": entry_long,
        "exit_long": 0.50,
        "entry_short": entry_short,
        "exit_short": 0.50,

        "prob_ewm_span": 8,
        "confirm_bars": 1,
        "allow_direct_flip": True,

        "min_hold": max(2, MIN_HOLD_BARS // 2),
        "enable_vol_spike": True,
        "vol_weight_gamma": 0.6,
        "neutral_to_long": False,
    }