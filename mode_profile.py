from config import SAFE_MODE, UP_PROBA_TH, DOWN_PROBA_TH, MIN_HOLD_BARS

def get_mode_params():
    # SAFE_MODE=True => conservative
    if SAFE_MODE:
        return {
            "ret_window": 6,
            "vol_window": 12,
            "sma_fast": 8,
            "sma_slow": 24,
            "autocorr_window": 24,
            "up_th": max(UP_PROBA_TH, 0.60),
            "down_th": min(DOWN_PROBA_TH, 0.40),
            "min_hold": max(MIN_HOLD_BARS, 6),
            "enable_vol_spike": False,
            "vol_weight_gamma": 0.0,
            "neutral_to_long": False, 
        }

    # SAFE_MODE=False => aggressive / volatility-sensitive
    return {
        "ret_window": 3,
        "vol_window": 8,
        "sma_fast": 6,
        "sma_slow": 18,
        "autocorr_window": 12,
        "up_th": min(0.55, UP_PROBA_TH - 0.05),
        "down_th": max(0.45, DOWN_PROBA_TH + 0.05),
        "min_hold": min(3, max(1, MIN_HOLD_BARS // 2)),
        "enable_vol_spike": True,
        "vol_weight_gamma": 0.6,
        "neutral_to_long": True,   # neutral => stay long
    }