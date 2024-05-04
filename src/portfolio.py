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
    df = pull_stock_data(tickers=ticks, start="2016-01-01", end="2024-01-01") # Dataframe of Prices
    amount_per_stock = allocation / len(ticks)
    cash = allocation

    # Populate portfolio dataframe
    portfolio_data = []
    date = df.index[0] # First Date of Portfolio
    data = df.loc[date] # Data for First Date

    for ticker in ticks:
        price = data.loc[('Adj Close', ticker)]
        quantity = math.floor(amount_per_stock / price)
        total_value = quantity * price
        cash -= total_value
        weight = total_value / allocation # Equal Weighted Portfolio
        portfolio_data.append({
                "Date": date,
                "Ticker": ticker,
                "Quantity": quantity,
                "Price": price,
                "Total Value": total_value,
                "Weight": weight
            })
    # Update CASH position
    portfolio_data.append({"Date": date,
                           "Ticker": "CASH", 
                           "Quantity": 0, 
                           "Price": 0, 
                           "Total Value": cash, 
                           "Weight": cash / allocation})
    portfolio = pd.DataFrame(portfolio_data)
    
    portfolio['Date'] = pd.to_datetime(portfolio['Date']) # Convert 'Date' column to datetime dtype
    portfolio.set_index('Date', inplace=True) # Set 'Date' column as index
    return portfolio

def update_portfolio(portfolio: pd.DataFrame) -> pd.DataFrame:
    """ Add a row for the CASH position in the Portfolio on the latest date

    Args:
        portfolio (pd.DataFrame): Dataframe of Portfolio

    Returns:
        pd.DataFrame: Dataframe of Portfolio
    """
    #
    return portfolio
