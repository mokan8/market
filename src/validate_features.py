"""
Validate derived feature matrix for S&P 500 volatility modeling.

Input:
  data/features/sp500_features.csv

This script is READ-ONLY and performs sanity checks only.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def main() -> None:
    path = Path("data/features/sp500_features.csv")

    if not path.exists():
        raise FileNotFoundError(f"Missing features file: {path}")

    df = pd.read_csv(path, index_col=0, parse_dates=True)

    print("=== SHAPE ===")
    print(df.shape)

    print("\n=== COLUMNS ===")
    print(list(df.columns))

    print("\n=== DATE RANGE ===")
    print(df.index.min().date(), "→", df.index.max().date())

    print("\n=== MISSING VALUES ===")
    print(df.isna().sum())

    if df.isna().any().any():
        raise RuntimeError("Found missing values in features.")

    print("\n=== BASIC DESCRIPTIVE STATS ===")
    print(df.describe())

    print("\n=== AUTOCORRELATION CHECKS ===")
    for col in ["r", "abs_r", "r2", "vol_20", "ewma_vol_94"]:
        ac = df[col].autocorr(lag=1)
        print(f"lag-1 autocorr({col}): {ac:.3f}")

    print("\n=== CORRELATION MATRIX (vol-related) ===")
    vol_cols = ["abs_r", "r2", "vol_20", "vol_60", "ewma_vol_94"]
    print(df[vol_cols].corr())

    print("\nOK ✅ feature validation passed")


if __name__ == "__main__":
    main()