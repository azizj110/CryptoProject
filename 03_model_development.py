

import json
import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV

from config import (
    PROCESSED_DIR,
    OUTPUT_DIR,
    ARTIFACTS_DIR,
    RANDOM_STATE,
    TRAINING_STRATEGY,
    REFIT_EVERY,
    ROLLING_WINDOW,
    TRAIN_START,
    TRAIN_END,
    TEST_START,
    TEST_END,
)
from utils import ensure_directories
from mode_profile import get_mode_params

MODE = get_mode_params()

def _json_safe(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        if isinstance(v, (np.integer,)):
            out[k] = int(v)
        elif isinstance(v, (np.floating,)):
            out[k] = float(v)
        else:
            out[k] = v
    return out


def _prob_up(model, X: pd.DataFrame) -> np.ndarray:
    p = model.predict_proba(X)
    cls = list(model.classes_)
    if 1 in cls:
        return p[:, cls.index(1)]
    return np.zeros(len(X))


def load_full_data() -> pd.DataFrame:
    features = pd.read_csv(PROCESSED_DIR / "features.csv", index_col=0, parse_dates=True)
    labels = pd.read_csv(PROCESSED_DIR / "labels.csv", index_col=0, parse_dates=True)

    use_label_cols = [c for c in ["label", "horizon", "t_value", "future_ret"] if c in labels.columns]
    data = features.join(labels[use_label_cols], how="inner")

    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    data = data[data["label"].isin([-1, 1])].copy()
    data["label"] = data["label"].astype(int)
    data = data.sort_index()
    return data


def _volatility_sample_weight(X: pd.DataFrame):
    gamma = MODE["vol_weight_gamma"]
    if gamma <= 0 or "vol_12" not in X.columns:
        return None

    v = pd.to_numeric(X["vol_12"], errors="coerce").fillna(0.0)
    med = v.median()
    mad = (v - med).abs().median()
    z = (v - med) / (1.4826 * mad + 1e-12)
    z = z.clip(lower=0, upper=3)
    w = 1.0 + gamma * z
    return w.to_numpy(dtype=float)


def tune_rf(X_train: pd.DataFrame, y_train: pd.Series):
    default_params = {
        "n_estimators": 400,
        "max_depth": 6,
        "min_samples_leaf": 5,
        "max_features": "sqrt",
    }

    if len(X_train) < 500 or y_train.nunique() < 2:
        return default_params, np.nan

    base = RandomForestClassifier(
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced_subsample",
    )

    param_dist = {
        "n_estimators": [200, 400, 700],
        "max_depth": [4, 6, 10, None],
        "min_samples_leaf": [1, 3, 5, 10],
        "max_features": ["sqrt", 0.5, 1.0],
    }

    n_splits = min(4, max(2, len(X_train) // 800))
    cv = TimeSeriesSplit(n_splits=n_splits)

    search = RandomizedSearchCV(
        estimator=base,
        param_distributions=param_dist,
        n_iter=15,
        scoring="f1_macro",
        n_jobs=-1,
        cv=cv,
        random_state=RANDOM_STATE,
    )
    sw = _volatility_sample_weight(X_train)
    if sw is None:
        search.fit(X_train, y_train)
    else:
        search.fit(X_train, y_train, sample_weight=sw)
    return search.best_params_, search.best_score_


def walk_forward_predict(
    X: pd.DataFrame,
    y: pd.Series,
    split_idx: int,
    params: dict,
    strategy: str,
    refit_every: int,
    rolling_window: int,
):
    test_idx = X.index[split_idx:]
    y_pred = pd.Series(index=test_idx, dtype=int)
    y_prob = pd.Series(index=test_idx, dtype=float)

    for start in range(split_idx, len(X), refit_every):
        end = min(start + refit_every, len(X))
        train_start = 0 if strategy == "expanding" else max(0, start - rolling_window)

        X_tr = X.iloc[train_start:start]
        y_tr = y.iloc[train_start:start]
        X_block = X.iloc[start:end]

        if len(X_tr) < 300 or y_tr.nunique() < 2:
            fallback = int(y_tr.mode().iloc[0]) if len(y_tr) else 1
            y_pred.loc[X_block.index] = fallback
            y_prob.loc[X_block.index] = 0.5
            continue

        model = RandomForestClassifier(
            **params,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            class_weight="balanced_subsample",
        )
        sw_tr = _volatility_sample_weight(X_tr)
        if sw_tr is None:
            model.fit(X_tr, y_tr)
        else:
            model.fit(X_tr, y_tr, sample_weight=sw_tr)
        y_pred.loc[X_block.index] = model.predict(X_block)
        y_prob.loc[X_block.index] = _prob_up(model, X_block)

    return y_pred.astype(int), y_prob.astype(float)


def main():
    ensure_directories()

    data = load_full_data()

    train_start = pd.Timestamp(TRAIN_START)
    train_end = pd.Timestamp(TRAIN_END)
    test_start = pd.Timestamp(TEST_START)
    test_end = pd.Timestamp(TEST_END)

    train_data = data[(data.index >= train_start) & (data.index <= train_end)].copy()
    test_data = data[(data.index >= test_start) & (data.index <= test_end)].copy()

    if len(train_data) == 0:
        raise ValueError("No training rows in 2018-2020 after cleaning.")
    if len(test_data) == 0:
        raise ValueError("No test rows in 2021 after cleaning.")

    drop_cols = ["label", "close", "market_ret_1", "horizon", "t_value", "future_ret"]
    feature_cols = [c for c in data.columns if c not in drop_cols]

    X_train = train_data[feature_cols]
    y_train = train_data["label"].astype(int)

    X_test = test_data[feature_cols]
    y_test = test_data["label"].astype(int)

    best_params, cv_score = tune_rf(X_train, y_train)

    if TRAINING_STRATEGY == "one_time":
        model = RandomForestClassifier(
            **best_params,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            class_weight="balanced_subsample",
        )
        sw_train = _volatility_sample_weight(X_train)
        if sw_train is None:
            model.fit(X_train, y_train)
        else:
            model.fit(X_train, y_train, sample_weight=sw_train)
        y_pred = pd.Series(model.predict(X_test), index=X_test.index)
        y_prob = pd.Series(_prob_up(model, X_test), index=X_test.index)

    elif TRAINING_STRATEGY in ["expanding", "rolling"]:
        combined = pd.concat([train_data, test_data], axis=0).sort_index()
        X_combined = combined[feature_cols]
        y_combined = combined["label"].astype(int)
        split_idx = len(train_data)

        y_pred_all, y_prob_all = walk_forward_predict(
            X=X_combined,
            y=y_combined,
            split_idx=split_idx,
            params=best_params,
            strategy=TRAINING_STRATEGY,
            refit_every=REFIT_EVERY,
            rolling_window=ROLLING_WINDOW,
        )
        y_pred = y_pred_all.reindex(X_test.index).astype(int)
        y_prob = y_prob_all.reindex(X_test.index).astype(float)

        model = RandomForestClassifier(
            **best_params,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            class_weight="balanced_subsample",
        )
        model.fit(X_train, y_train)
    else:
        raise ValueError("TRAINING_STRATEGY must be one_time / expanding / rolling")

    joblib.dump(model, ARTIFACTS_DIR / "rf_model.pkl")
    X_train.to_csv(ARTIFACTS_DIR / "X_train.csv")
    X_test.to_csv(ARTIFACTS_DIR / "X_test.csv")
    y_train.to_frame("label").to_csv(ARTIFACTS_DIR / "y_train.csv")
    y_test.to_frame("label").to_csv(ARTIFACTS_DIR / "y_test.csv")

    pred = pd.DataFrame(index=X_test.index)
    pred["y_true"] = y_test
    pred["y_pred"] = y_pred
    pred["y_prob_up"] = y_prob
    pred["market_ret_1"] = test_data["market_ret_1"]
    pred["close"] = test_data["close"]
    pred.to_csv(OUTPUT_DIR / "predictions.csv")

    meta = {
        "training_strategy": TRAINING_STRATEGY,
        "train_period": [str(train_data.index.min()), str(train_data.index.max())],
        "test_period": [str(test_data.index.min()), str(test_data.index.max())],
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "best_params": _json_safe(best_params),
        "cv_f1_macro": None if pd.isna(cv_score) else float(cv_score),
    }
    with open(OUTPUT_DIR / "model_meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"[OK] Train rows: {len(X_train)} | Test rows: {len(X_test)}")
    print(f"[OK] Train period: {train_data.index.min()} -> {train_data.index.max()}")
    print(f"[OK] Test period:  {test_data.index.min()} -> {test_data.index.max()}")
    print(f"[OK] Saved: {OUTPUT_DIR / 'predictions.csv'}")


if __name__ == "__main__":
    main()