import yfinance as yf

stock = "AAPL"

df = yf.download(
    stock,
    start="2015-01-01",
    end="2026-01-01",
    auto_adjust=False
)

# MultiIndex hatao je exist karda hove
if hasattr(df.columns, "droplevel"):
    try:
        df.columns = df.columns.droplevel(1)
    except:
        pass

df.reset_index(inplace=True)

print(df.head())

df.to_csv("data/stock_data.csv", index=False)