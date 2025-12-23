import numpy as np
import pandas as pd


def main():
    prices_path = "data/raw/sp500_adj_close.csv"
    returns_path = "data/raw/sp500_log_returns.csv"

    prices = pd.read_csv(prices_path, index_col=0, parse_dates=True)
    returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)

    if prices.shape[1] != 1:
        raise RuntimeError("Expected 1 column in prices file")

    if returns.shape[1] != 1:
        raise RuntimeError("Expected 1 column in returns file")

    p = prices.iloc[:, 0]
    r = returns.iloc[:, 0]

    print("=== SHAPES ===")
    print("prices:", prices.shape)
    print("returns:", returns.shape)

    print("\n=== DATE RANGES ===")
    print("prices:", p.index.min().date(), "→", p.index.max().date())
    print("returns:", r.index.min().date(), "→", r.index.max().date())

    print("\n=== MISSING VALUES ===")
    print("prices NaN:", int(p.isna().sum()))
    print("returns NaN:", int(r.isna().sum()))

    print("\n=== BASIC SANITY CHECKS ===")
    if (p <= 0).any():
        raise RuntimeError("Found non-positive prices")

    if not np.isfinite(r).all():
        raise RuntimeError("Found non-finite values in returns")

    print("\n=== RETURN SUMMARY ===")
    print(r.describe())

    print("\n=== DEPENDENCE CHECKS ===")
    print("lag-1 autocorr(r):", r.autocorr(1))
    print("lag-1 autocorr(|r|):", r.abs().autocorr(1))

    print("\n=== CONSISTENCY CHECK ===")
    r_from_prices = np.log(p / p.shift(1)).dropna()
    aligned = pd.concat([r, r_from_prices], axis=1, join="inner")
    max_diff = (aligned.iloc[:, 0] - aligned.iloc[:, 1]).abs().max()
    print("max |return - log(price ratio)|:", max_diff)

    print("\nOK ✅ data validation passed")


if __name__ == "__main__":
    main()