""" Portfolio Attribution Project
"""
from portfolio import create_portfolio
from user_input import get_tickers
from user_input import get_portfolio_allocation
from pull_data import pull_stock_data

def main():
    """
    Main Function for Portfolio Attribution Project
    """
    ticks = get_tickers() # Tickers as a List
    allocation = get_portfolio_allocation() # Integer Dollar Ammount
    price_df = pull_stock_data(tickers=ticks,
                               start="2016-01-01",
                                end="2024-01-01") # Dataframe of Prices
    portfolio = create_portfolio(df=price_df, allocation=allocation, ticks=ticks)
    print(portfolio)
    return None

if __name__== "__main__":
    main()
