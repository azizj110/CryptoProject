# run_all.py
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RUN_ORDER = [
    "01_feature_engineering.py",
    "02_labeling_trend_scanning.py",
    "03_model_development.py",
    "04_feature_importance.py",
    "05_model_evaluation.py",
    "06_backtest_optional.py",
]

print("Run order:")
for i, s in enumerate(RUN_ORDER, start=1):
    print(f"{i}. {s}")

for s in RUN_ORDER:
    script_path = BASE_DIR / s
    if not script_path.exists():
        raise SystemExit(f"Missing file: {script_path}")

    print(f"\n=== Running {s} ===")
    res = subprocess.run([sys.executable, s], cwd=BASE_DIR)
    if res.returncode != 0:
        raise SystemExit(f"{s} failed with code {res.returncode}")

print("\nPipeline completed.")