import yfinance as yf
import os

# Data folder create if not exists
os.makedirs("data", exist_ok=True)

stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

for stock in stocks:
    print(f"Downloading {stock}...")

    df = yf.download(
        stock,
        start="2015-01-01",
        end="2025-12-31",
        auto_adjust=False
    )

    df.reset_index(inplace=True)

    file_path = f"data/{stock}.csv"
    df.to_csv(file_path, index=False)

    print(f"Saved: {file_path}")

print("\nAll datasets downloaded successfully!")