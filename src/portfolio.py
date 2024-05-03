""" Create a Portfolio
"""
import math
import pandas as pd
from user_input import get_tickers
from user_input import get_portfolio_allocation
from pull_data import pull_stock_data


def create_portfolio() -> pd.DataFrame:
    """ Create a Portfolio - Initially this will be an equal weighted portfolio
    Args:

    Returns:
        dict: Dataframe of Portfolio
    """
    ticks = get_tickers() # Tickers as a List
    allocation = get_portfolio_allocation() # Integer Dollar Ammount
    df = pull_stock_data(tickers=ticks,
                           start="2016-01-01",
                           end="2024-01-01") # Dataframe of Prices

    amount_per_stock = allocation / len(ticks)

    # Populate portfolio dataframe
    portfolio_data = []
    date = df.index[0] # First Date of Portfolio
    data = df.loc[date] # Data for First Date

    for ticker in ticks:
        price = data.loc[('Adj Close', ticker)]
        quantity = math.floor(amount_per_stock / price)
        total_value = amount_per_stock
        weight = 1 / len(ticks) # Equal Weighted Portfolio
        portfolio_data.append({
                "Date": date,
                "Ticker": ticker,
                "Quantity": quantity,
                "Price": price,
                "Total Value": total_value,
                "Weight": str(weight * 100) + '%'
            })
    portfolio = pd.DataFrame(portfolio_data)

    return portfolio
