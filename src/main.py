""" Portfolio Attribution Project
"""
from eq_weighted_portfolio import create_portfolio
from user_input import get_tickers
from user_input import get_portfolio_allocation
from pull_data import pull_stock_data

def main():
    """
    Main Function for Portfolio Attribution Project
    """
    # Tickers as a List
    ticks = get_tickers()
    # Integer Dollar Ammount
    allocation = get_portfolio_allocation()
    # Dataframe of Prices
    price_df = pull_stock_data(tickers=ticks,
                               start="2016-01-04",
                                end="2016-01-10")
    # Create Portfolio
    portfolio = create_portfolio(price_df=price_df, allocation=allocation, ticks=ticks)
    print(portfolio)
    return None

if __name__== "__main__":
    main()
