""" Create a Portfolio
"""
import math
from datetime import timedelta
import pandas as pd


def create_portfolio(price_df: pd.DataFrame, allocation: str, ticks: list) -> pd.DataFrame:
    """ Create an Equal Weighted Portfolio
    Args:

    Returns:
        dict: Dataframe of Portfolio
    """
    portfolio = initialize_portfolio(
        price_df=price_df, allocation=allocation, ticks=ticks)
    print("PORTFOLIO INITIALIZED")
    print(portfolio)
    # Rebalance for each date after the first one
    for date in price_df.index.unique()[1:]:
        #print("UPDATE PORTFOLIO")
        portfolio = update_portfolio(portfolio=portfolio.copy(),
                                     price_df=price_df,
                                     ticks=ticks,
                                     date=date)
    return portfolio


def initialize_portfolio(price_df: pd.DataFrame,
                         allocation: str,
                         ticks: list) -> pd.DataFrame:
    """ Initialize the portfolio for the first date

    Args:
        df (pd.DataFrame): Price Dataframe
        allocation (str): Dollar Amount for the Portfolio
        ticks (list): List of Tickers provided by the user

    Returns:
        pd.DataFrame: Portfolio of Tickers and CASH position
    """
    amount_per_stock = allocation / len(ticks)
    cash = allocation

    # Populate portfolio dataframe
    portfolio_data = []
    date = price_df.index[0]  # First Date of Portfolio
    data = price_df.loc[date]  # Data for First Date

    # Update Stock positions
    for ticker in ticks:
        price = data.loc[('Adj Close', ticker)]
        quantity = math.floor(amount_per_stock / price)
        total_value = quantity * price
        cash -= total_value
        weight = total_value / allocation  # Equal Weighted Portfolio
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
                           "Quantity": cash,
                           "Price": 1,
                           "Total Value": cash,
                           "Weight": cash / allocation})
    portfolio = pd.DataFrame(portfolio_data)

    # Convert 'Date' column to datetime dtype
    portfolio['Date'] = pd.to_datetime(portfolio['Date'])
    # Set 'Date' and 'Ticker' column as index
    portfolio.set_index(['Date', 'Ticker'], inplace=True)

    return portfolio


def update_portfolio(portfolio: pd.DataFrame,
                     price_df: pd.DataFrame,
                     ticks: list,
                     date) -> pd.DataFrame:
    """ Add a row for the CASH position in the Portfolio on the latest date

    Args:
        portfolio (pd.DataFrame): Dataframe of Portfolio

    Returns:
        pd.DataFrame: Dataframe of Portfolio
    """
    for ticker in ticks:
        # Get new price, update dataframe and calculate new portfolio value
        new_price = price_df.loc[date, ('Adj Close', ticker)]

        prev_date = date - timedelta(days=1)
        try:
            prev_quantity = portfolio.loc[(
                prev_date, ticker)]["Quantity"]
            prev_weight = portfolio.loc[(
                prev_date), ticker]["Weight"]
        except KeyError:
            #print(f"Date not found - {prev_date} must be a holiday")
            prev_date -= timedelta(days=1)
            #print(f"New Prev Date: {prev_date}")
            while (prev_date, ticker) not in portfolio.index:
                prev_date -= timedelta(days=1)
            #print(f"Previous Date Found: {prev_date}")
            if (prev_date, ticker) in portfolio.index:
                prev_quantity = portfolio.loc[(
                prev_date, ticker)]["Quantity"]
            prev_weight = portfolio.loc[(
                prev_date), ticker]["Weight"]

        new_value = prev_quantity * new_price
   
        portfolio.loc[(date, ticker), 'Quantity'] = prev_quantity
        portfolio.loc[(date, ticker), 'Price'] = new_price
        portfolio.loc[(date, ticker), 'Total Value'] = new_value
        portfolio.loc[(date, ticker), 'Weight'] = prev_weight

    # Update CASH in dataframe
    portfolio.loc[(date, "CASH"), 'Quantity'] = portfolio.loc[(prev_date, "CASH"), 'Quantity']
    portfolio.loc[(date, "CASH"), 'Price'] = portfolio.loc[(prev_date, "CASH"), 'Price']
    portfolio.loc[(date, "CASH"), 'Total Value'] = portfolio.loc[(prev_date, "CASH"), 'Total Value']
    portfolio.loc[(date, "CASH"), 'Weight'] = portfolio.loc[(prev_date, "CASH"), 'Weight']

    #print("TRIGGER PORTFOLIO REBALANCING")
    rebalance_portfolio(portfolio=portfolio,
                        ticks=ticks,
                        date=date)

    return portfolio


def rebalance_portfolio(portfolio: pd.DataFrame,
                        ticks: list,
                        date) -> pd.DataFrame:
    """ Rebalance the Portfolio for the most latest date 

    Args:
        portfolio (pd.DataFrame): Portfolio dataframe
        price_df (pd.DataFrame): Price dataframe
        tickers (list): List of Tickers
        date (_type_): Date to rebalance on

    Returns:
        pd.DataFrame: Rebalanced Portfolio
    """
    portfolio_value = portfolio.loc[date]["Total Value"].sum()
    cash = portfolio_value
    #print(f"Portfolio Value: {portfolio_value} on {date}")
    amount_per_stock = portfolio_value/len(ticks)

    # Update Stock positions
    for ticker in ticks:
        # Calculate Portfolio Metrics
        price = portfolio.loc[(date, ticker), 'Price']
        quantity = math.floor(amount_per_stock / price)
        total_value = quantity * price
        weight = total_value / portfolio_value
        # Update values in dataframe
        portfolio.loc[(date, ticker), 'Quantity'] = quantity
        portfolio.loc[(date, ticker), 'Total Value'] = total_value
        portfolio.loc[(date, ticker), 'Weight'] = weight
        # update cash amount
        cash -= total_value

    # Update CASH in dataframe
    portfolio.loc[(date, "CASH"), 'Quantity'] = cash
    portfolio.loc[(date, "CASH"), 'Price'] = 1.0
    portfolio.loc[(date, "CASH"), "Total Value"] = cash
    portfolio.loc[(date, "CASH"), "Weight"] = cash / portfolio_value

    #print(portfolio)

    return portfolio
