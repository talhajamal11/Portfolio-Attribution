""" Portfolio Attribution Project
"""
from pull_data import pull_stock_data
from pull_data import one_stock_data

def main():
    print("------- Downloading Stock Data --------")
    stocks = ["TSLA", "MSFT"]
    data = pull_stock_data(tickers=stocks,
                           start="2016-01-01",
                           end="2024-01-01")
    tsla = one_stock_data(dataframe=data,
                          ticker="TSLA")
    print(tsla)
    return None

if __name__== "__main__":
    main()
