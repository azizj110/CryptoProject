# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_PATH = BASE_DIR / "prices.csv"

PROCESSED_DIR = BASE_DIR / "processed"
OUTPUT_DIR = BASE_DIR / "outputs"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

RANDOM_STATE = 42
TEST_SIZE = 0.20

# Trend scanning
MIN_TREND_H = 6
MAX_TREND_H = 36
TREND_STEP = 1
T_VALUE_MIN = 0.0

# Training strategy: one_time | expanding | rolling
TRAINING_STRATEGY = "one_time"
REFIT_EVERY = 24
ROLLING_WINDOW = 24 * 60

# Required fixed periods (assignment)
TRAIN_START = "2018-01-01 00:00:00"
TRAIN_END = "2020-12-31 23:59:59"
TEST_START = "2021-01-01 00:00:00"
TEST_END = "2021-12-31 23:59:59"

# Optional backtest
COST_BPS = 5
UP_PROBA_TH = 0.60
DOWN_PROBA_TH = 0.40

LONG_ONLY = True
MIN_HOLD_BARS = 6

# Sensitivity mode:
# False -> keep current behavior
# True  -> more sensitive to volatility/price variation
SAFE_MODE = False