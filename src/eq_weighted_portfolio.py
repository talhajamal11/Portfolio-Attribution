""" Create a Portfolio
"""
import math
from datetime import datetime, timedelta
import pandas as pd

def create_portfolio(price_df: pd.DataFrame, allocation: str, ticks: list) -> pd.DataFrame:
    """ Create an Equal Weighted Portfolio
    Args:

    Returns:
        dict: Dataframe of Portfolio
    """
    print("INITIALIZE PORTFOLIO")
    portfolio = initialize_portfolio(price_df=price_df, allocation=allocation, ticks=ticks)
    print("PORTFOLIO INITIALIZED")
    print(portfolio)
    # Rebalance for each date after the first one
    for date in price_df.index.unique()[1:]:
        print("UPDATE PORTFOLIO")
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
    date = price_df.index[0] # First Date of Portfolio
    data = price_df.loc[date] # Data for First Date

    # Update Stock positions
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
                           "Quantity": cash, 
                           "Price": 1, 
                           "Total Value": cash, 
                           "Weight": cash / allocation})
    portfolio = pd.DataFrame(portfolio_data)

    portfolio['Date'] = pd.to_datetime(portfolio['Date']) # Convert 'Date' column to datetime dtype
    portfolio.set_index(['Date', 'Ticker'], inplace=True) # Set 'Date' and 'Ticker' column as index

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
        new_price = price_df.loc[date, ('Adj Close', ticker)]
        print("NEW PRICE RETRIEVED", new_price)
        prev_quantity = portfolio.loc[(date - timedelta(days=1), ticker)]["Quantity"]
        print("PREV QUANTITY RETRIEVED", prev_quantity)
        new_value = prev_quantity * new_price
        #new_weight = portfolio[portfolio["Ticker"] == ticker]["Weight"].iloc[0]
        prev_weight = portfolio.loc[(date - timedelta(days=1)), ticker]["Weight"]
        print("OLD WEIGHT RETRIEVED", prev_weight)
        #portfolio.loc[len(portfolio.index)] = new_row_data
        #portfolio.rename(index={portfolio.index[-1]: date}, inplace=True) # Update Index of new row
        portfolio.loc[(date, ticker), 'Quantity'] = prev_quantity
        portfolio.loc[(date, ticker), 'Price'] = new_price
        portfolio.loc[(date, ticker), 'Total Value'] = new_value
        portfolio.loc[(date, ticker), 'Weight'] = prev_weight
    # Add CASH
    # Get the row corresponding to "CASH"

    print(portfolio)

    print("UPDATE CASH")
    #cash_row = portfolio[portfolio['Ticker'] == 'CASH'].iloc[-1]
    #portfolio.loc[len(portfolio.index)] = cash_row
    #portfolio.rename(index={portfolio.index[-1]: date}, inplace=True)

    portfolio.loc[(date, "CASH"), 'Quantity'] = portfolio.loc[(date - timedelta(days=1), "CASH"), 'Quantity']
    portfolio.loc[(date, "CASH"), 'Price'] = portfolio.loc[(date - timedelta(days=1), "CASH"), 'Price']
    portfolio.loc[(date, "CASH"), 'Total Value'] = portfolio.loc[(date - timedelta(days=1), "CASH"), 'Total Value']
    portfolio.loc[(date, "CASH"), 'Weight'] = portfolio.loc[(date - timedelta(days=1), "CASH"), 'Weight']
    print(portfolio)

    print("TRIGGER PORTFOLIO REBALANCING")
    rebalance_portfolio(portfolio=portfolio,
                        ticks=ticks,
                        date=date)

    return portfolio

def rebalance_portfolio(portfolio:pd.DataFrame,
                        ticks: list, date) -> pd.DataFrame:
    """ Rebalance the Portfolio for the most latest date 

    Args:
        portfolio (pd.DataFrame): Portfolio dataframe
        price_df (pd.DataFrame): Price dataframe
        tickers (list): List of Tickers
        date (_type_): Date to rebalance on

    Returns:
        pd.DataFrame: Rebalanced Portfolio
    """
    #portfolio_latest_date = portfolio.loc[date]
    portfolio_value = portfolio.loc[date]["Total Value"].sum()
    print(f"New Portfolio Value: {portfolio_value}")
    amount_per_stock = portfolio_value/len(ticks)

    # Update Stock positions
    for ticker in ticks:
        temp_df = portfolio.loc[date]
        price = temp_df[temp_df["Ticker"] == ticker]["Price"].iloc[0]
        quantity = math.floor(amount_per_stock / price)
        total_value = quantity * price
        weight = total_value / portfolio_value
        print(f"For {ticker} the new price is {price} and quantity is {quantity}\
               and total value is {total_value} and weight is {weight}")
        # Update Values

    return None
