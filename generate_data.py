"""
Download S&P 500 data and compute daily log returns (2000–present).
Outputs:
  data/sp500_adj_close.csv
  data/sp500_log_returns.csv
"""

from pathlib import Path

import numpy as np
import yfinance as yf
import pandas as pd


def main() -> None:
    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)

    ticker = "^GSPC"
    start = "2000-01-01"

    df = yf.download(ticker, start=start, auto_adjust=True, progress=False)

    if df is None or df.empty:
        raise RuntimeError("Download returned empty dataframe. Check internet / ticker.")

    # With auto_adjust=True, 'Close' is already adjusted; 'Adj Close' is usually absent.
    if "Close" not in df.columns:
        raise RuntimeError(f"Expected 'Close' column, got columns: {list(df.columns)}")

    prices = df["Close"].squeeze("columns").dropna().rename("adj_close")
    returns = np.log1p(prices.pct_change()).dropna().rename("log_return")

    prices.to_csv(out_dir / "sp500_adj_close.csv")
    returns.to_csv(out_dir / "sp500_log_returns.csv")
    pd.concat([prices, returns], axis=1).to_csv(out_dir / "sp500_prices_and_returns.csv")

    print("Saved:")
    print(
        f"  {out_dir/'sp500_adj_close.csv'}  rows={len(prices)}  "
        f"start={prices.index.min().date()}  end={prices.index.max().date()}"
    )
    print(
        f"  {out_dir/'sp500_log_returns.csv'} rows={len(returns)} "
        f"start={returns.index.min().date()} end={returns.index.max().date()}"
    )
    print("\nReturns summary:")
    print(returns.describe())


if __name__ == "__main__":
    main()