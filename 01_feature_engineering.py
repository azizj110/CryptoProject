

import warnings
import numpy as np
import pandas as pd
from mode_profile import get_mode_params

from config import RAW_DATA_PATH, PROCESSED_DIR
from utils import ensure_directories, load_prices, rsi

try:
    from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
    HAS_STATSMODELS = True
except Exception:
    HAS_STATSMODELS = False


def _as_prob_df(probs, index):
    if isinstance(probs, pd.DataFrame):
        out = probs.copy()
        out.index = index
        return out
    arr = np.asarray(probs)
    if arr.ndim == 1:
        arr = arr.reshape(-1, 1)
    return pd.DataFrame(arr, index=index, columns=list(range(arr.shape[1])))


def _fallback_regime(ret: pd.Series) -> pd.Series:
    rv = ret.rolling(24).std()
    baseline = rv.rolling(24 * 10).median()
    return (rv > baseline).astype(float).ffill().fillna(0.0)


def markov_regime_probability(ret_1: pd.Series, train_ratio: float = 0.7) -> pd.Series:
    out = pd.Series(index=ret_1.index, dtype=float)
    ret = ret_1.dropna()

    if (not HAS_STATSMODELS) or len(ret) < 300:
        out.loc[ret.index] = _fallback_regime(ret)
        return out.ffill().fillna(0.0).clip(0.0, 1.0)

    split = int(len(ret) * train_ratio)
    train = ret.iloc[:split]

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            mod_train = MarkovRegression(train, k_regimes=2, trend="c", switching_variance=True)
            res_train = mod_train.fit(disp=False, maxiter=250)

        train_probs = _as_prob_df(res_train.filtered_marginal_probabilities, train.index)
        train_state = train_probs.idxmax(axis=1)

        state_var = {}
        for s in train_probs.columns:
            vals = train[train_state == s]
            state_var[s] = vals.var() if len(vals) >= 20 else -np.inf
        high_vol_state = max(state_var, key=state_var.get)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            mod_full = MarkovRegression(ret, k_regimes=2, trend="c", switching_variance=True)
            res_full = mod_full.filter(res_train.params)

        full_probs = _as_prob_df(res_full.filtered_marginal_probabilities, ret.index)
        out.loc[ret.index] = full_probs[high_vol_state].astype(float)

    except Exception:
        out.loc[ret.index] = _fallback_regime(ret)

    return out.ffill().fillna(0.0).clip(0.0, 1.0)


def build_features(prices: pd.DataFrame) -> pd.DataFrame:
    mode = get_mode_params()

    feat = pd.DataFrame(index=prices.index)
    close = prices["close"]
    ret_1 = close.pct_change()

    feat["ret_1"] = ret_1
    feat["ret_6"] = close.pct_change(mode["ret_window"])
    feat["vol_12"] = ret_1.rolling(mode["vol_window"]).std()
    feat["rsi_14"] = rsi(close, 14)

    sma_fast = close.rolling(mode["sma_fast"]).mean()
    sma_slow = close.rolling(mode["sma_slow"]).mean()
    feat["ma_gap_8_24"] = sma_fast / sma_slow - 1.0
    feat["ma_cross_8_24"] = (sma_fast > sma_slow).astype(int)

    feat["autocorr_24_lag1"] = ret_1.rolling(mode["autocorr_window"]).corr(ret_1.shift(1))
    feat["ret_lag1"] = ret_1.shift(1)

    # Extra volatility sensitivity only when SAFE_MODE=True
    if mode["enable_vol_spike"]:
        feat["vol_spike"] = (ret_1.abs() / (feat["vol_12"] + 1e-12)).clip(0, 10)
    else:
        feat["vol_spike"] = 0.0

    feat["regime_prob_high_vol"] = markov_regime_probability(ret_1)
    feat["regime_state_high_vol"] = (feat["regime_prob_high_vol"] >= 0.5).astype(int)

    feat["close"] = close
    feat["market_ret_1"] = ret_1

    feat = feat.replace([np.inf, -np.inf], np.nan)
    return feat


def main():
    ensure_directories()
    prices = load_prices(RAW_DATA_PATH)
    features = build_features(prices)
    features.to_csv(PROCESSED_DIR / "features.csv")
    print(f"[OK] Saved: {PROCESSED_DIR / 'features.csv'} | shape={features.shape}")


if __name__ == "__main__":
    main()