""" Portfolio Attribution Project
"""
from user_input import get_tickers
from pull_data import pull_stock_data
from pull_data import one_stock_data

def main():
    """
    Main Function for Portfolio Attribution Project
    """
    ticks = get_tickers()
    data = pull_stock_data(tickers=ticks,
                           start="2016-01-01",
                           end="2024-01-01")
    print(data)
    return None

if __name__== "__main__":
    main()
