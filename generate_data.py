"""
Download S&P 500 data and compute daily log returns (2000–present).
Outputs:
  data/raw/sp500_adj_close.csv
  data/raw/sp500_log_returns.csv
  data/raw/sp500_prices_and_returns.csv
"""

from pathlib import Path

import numpy as np
import yfinance as yf


def main() -> None:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    ticker = "^GSPC"
    start = "2000-01-01"

    df = yf.download(ticker, start=start, auto_adjust=True, progress=False)
    if df is None or df.empty:
        raise RuntimeError("Download returned empty dataframe. Check internet / ticker.")

    # With auto_adjust=True, 'Close' is already adjusted. Use squeeze in case yfinance returns a 1-col DataFrame.
    close = df["Close"].squeeze("columns")

    prices = close.dropna().rename("adj_close")
    returns = np.log(prices / prices.shift(1)).dropna().rename("log_return")

    prices.to_csv(out_dir / "sp500_adj_close.csv")
    returns.to_csv(out_dir / "sp500_log_returns.csv")
    (prices.to_frame().join(returns)).to_csv(out_dir / "sp500_prices_and_returns.csv")

    print("Saved:")
    print(f"  {out_dir/'sp500_adj_close.csv'}  rows={len(prices)}  start={prices.index.min().date()}  end={prices.index.max().date()}")
    print(f"  {out_dir/'sp500_log_returns.csv'} rows={len(returns)} start={returns.index.min().date()} end={returns.index.max().date()}")
    print(f"  {out_dir/'sp500_prices_and_returns.csv'} rows={len(prices.to_frame().join(returns))}")


if __name__ == "__main__":
    main()