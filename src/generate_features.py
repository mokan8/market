from pathlib import Path
import numpy as np
import pandas as pd


def main() -> None:
    in_path = Path("data/raw/sp500_log_returns.csv")
    out_dir = Path("data/features")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "sp500_features.csv"

    if not in_path.exists():
        raise FileNotFoundError(f"Missing input file: {in_path}")

    df = pd.read_csv(in_path, index_col=0, parse_dates=True)

    if df.shape[1] != 1:
        raise RuntimeError(f"Expected 1 column in returns file, got {list(df.columns)}")

    r = df.iloc[:, 0].astype(float).rename("r")

    feats = pd.DataFrame(index=r.index)
    feats["r"] = r
    feats["abs_r"] = r.abs()
    feats["r2"] = r**2

    # Rolling momentum (cumulative log return over window)
    feats["mom_5"] = r.rolling(5).sum()
    feats["mom_20"] = r.rolling(20).sum()
    feats["mom_60"] = r.rolling(60).sum()

    # Rolling volatility (std of log returns)
    feats["vol_20"] = r.rolling(20).std(ddof=0)
    feats["vol_60"] = r.rolling(60).std(ddof=0)

    # EWMA volatility (RiskMetrics-style; lambda ~ 0.94 is common for daily)
    lam = 0.94
    feats["ewma_var_94"] = r.pow(2).ewm(alpha=1 - lam, adjust=False).mean()
    feats["ewma_vol_94"] = np.sqrt(feats["ewma_var_94"])

    feats = feats.dropna()
    feats.to_csv(out_path)

    print("Saved features:")
    print(f"  {out_path} rows={len(feats)} cols={feats.shape[1]}")
    print(f"  start={feats.index.min().date()} end={feats.index.max().date()}")
    print("\nPreview:")
    print(feats.head())


if __name__ == "__main__":
    main()