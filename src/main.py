""" Portfolio Attribution Project
"""
from pull_data import pull_stock_data

def main():
    print("------- Downloading Stock Data --------")
    stocks = ["TSLA"]
    data = pull_stock_data(tickers=stocks,
                           start="2016-01-01",
                           end="2024-01-01")
    print(data.head())
    return None

if __name__== "__main__":
    main()
