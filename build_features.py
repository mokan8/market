"""
Download S&P 500 data and compute daily log returns (2000–present).
Outputs:
  data/sp500_adj_close.csv
  data/sp500_log_returns.csv
"""

import numpy as np
import pandas as pd
import yfinance as yf
from pathlib import Path


def main() -> None:
    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)

    ticker = "^GSPC"
    start = "2000-01-01"

    df = yf.download("^GSPC", start="2000-01-01", auto_adjust=True, progress=False)
    prices = df["Close"].dropna().rename("adj_close")
    returns = np.log(prices / prices.shift(1)).dropna().rename("log_return")

    if df is None or df.empty:
        raise RuntimeError("Download returned empty dataframe. Check internet / ticker.")

    prices = df["Adj Close"].dropna().rename("adj_close")
    returns = np.log(prices / prices.shift(1)).dropna().rename("log_return")

    prices.to_csv(out_dir / "sp500_adj_close.csv")
    returns.to_csv(out_dir / "sp500_log_returns.csv")

    print("Saved:")
    print(f"  {out_dir/'sp500_adj_close.csv'}  rows={len(prices)}  start={prices.index.min().date()}  end={prices.index.max().date()}")
    print(f"  {out_dir/'sp500_log_returns.csv'} rows={len(returns)} start={returns.index.min().date()} end={returns.index.max().date()}")
    print("\nReturns summary:")
    print(returns.describe())


if __name__ == "__main__":
    main()