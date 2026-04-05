# utils.py
import json
import numpy as np
import pandas as pd
from pathlib import Path

from config import PROCESSED_DIR, OUTPUT_DIR, ARTIFACTS_DIR


def ensure_directories() -> None:
    for p in [PROCESSED_DIR, OUTPUT_DIR, ARTIFACTS_DIR]:
        Path(p).mkdir(parents=True, exist_ok=True)


def _find_col(columns, candidates):
    lower = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand in lower:
            return lower[cand]
    for c in columns:
        cl = c.lower()
        if any(cand in cl for cand in candidates):
            return c
    return None


def load_prices(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("Input CSV is empty.")

    dt_col = _find_col(df.columns, ["date", "datetime", "timestamp", "time"])
    if dt_col is None:
        raise ValueError("Could not find a date/time column.")
    df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce", utc=True)
    df = df.dropna(subset=[dt_col]).sort_values(dt_col).set_index(dt_col)
    try:
        df.index = df.index.tz_convert(None)
    except Exception:
        pass

    coin_col = _find_col(df.columns, ["coin", "symbol", "asset"])
    if coin_col is not None and df[coin_col].nunique(dropna=True) > 1:
        keep = df[coin_col].dropna().astype(str).mode().iloc[0]
        df = df[df[coin_col].astype(str) == keep]

    rename_map = {}
    mapping = {
        "open": ["open", "open_price"],
        "high": ["high", "high_price"],
        "low": ["low", "low_price"],
        "close": ["close", "adj_close", "price"],
        "volume": ["volume", "vol", "base_volume"],
    }
    for std, cands in mapping.items():
        found = _find_col(df.columns, cands)
        if found is not None:
            rename_map[found] = std
    df = df.rename(columns=rename_map)

    if "close" not in df.columns:
        raise ValueError("No close column found.")
    if "volume" not in df.columns:
        df["volume"] = 0.0

    for c in ["open", "high", "low", "close", "volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["close"])
    df = df[~df.index.duplicated(keep="first")]
    return df


def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0.0)
    down = -delta.clip(upper=0.0)
    avg_gain = up.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    avg_loss = down.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    rs = avg_gain / (avg_loss + 1e-12)
    return 100 - (100 / (1 + rs))


def infer_bars_per_year(index, default: int = 24 * 365) -> int:
    if not isinstance(index, pd.DatetimeIndex) or len(index) < 3:
        return default
    deltas = index.to_series().diff().dropna().dt.total_seconds()
    med = deltas.median()
    if med is None or med <= 0:
        return default
    return int((365 * 24 * 3600) / med)