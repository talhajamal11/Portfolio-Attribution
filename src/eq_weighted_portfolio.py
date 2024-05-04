""" Create a Portfolio
"""
import math
import pandas as pd

def initialize_portfolio(df: pd.DataFrame, allocation: str, ticks: list) -> pd.DataFrame:
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
    date = df.index[0] # First Date of Portfolio
    data = df.loc[date] # Data for First Date

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
    portfolio.set_index('Date', inplace=True) # Set 'Date' column as index

    return portfolio

def update_portfolio(portfolio: pd.DataFrame, price_df: pd.DataFrame, ticks: list, date) -> pd.DataFrame:
    """ Add a row for the CASH position in the Portfolio on the latest date

    Args:
        portfolio (pd.DataFrame): Dataframe of Portfolio

    Returns:
        pd.DataFrame: Dataframe of Portfolio
    """
    for ticker in ticks:
        new_price = price_df.loc[('Adj Close', ticker)]
        print(f"New Price is {new_price}")
        prev_quantity = portfolio[portfolio["Ticker"] == ticker]["Quantity"].iloc[0]
        print(f"Prev Quantity: {prev_quantity}")
        new_value = prev_quantity * new_price
        print(f"New Value for {ticker} is {new_value}")
        new_weight = portfolio[portfolio["Ticker"] == ticker]["Weight"].iloc[0]
        new_row_data = {
            "Date": date,
            "Ticker": ticker, 
            "Quantity": prev_quantity, 
            "Price": new_price, 
            "Total Value": new_value, 
            "Weight": new_weight
        }
        portfolio.loc[len(portfolio.index)] = new_row_data
        portfolio.rename(index={portfolio.index[-1]: date}, inplace=True) # Update Index of new row
    # Add CASH
    # Get the row corresponding to "CASH"
    cash_row = portfolio[portfolio['Ticker'] == 'CASH'].iloc[-1]
    # Append the "CASH" row to the end of the DataFrame
    portfolio.loc[len(portfolio.index)] = cash_row
    portfolio.rename(index={portfolio.index[-1]: date}, inplace=True)
    return portfolio

def rebalance_portfolio(portfolio:pd.DataFrame, price_df: pd.DataFrame, tickers: list, date) -> pd.DataFrame:
    """ Rebalance the Portfolio for the most latest date 

    Args:
        portfolio (pd.DataFrame): Portfolio dataframe
        price_df (pd.DataFrame): Price dataframe
        tickers (list): List of Tickers
        date (_type_): Date to rebalance on

    Returns:
        pd.DataFrame: Rebalanced Portfolio
    """
    portfolio_latest_date = portfolio.loc[date]

    return None

def create_portfolio(df: pd.DataFrame, allocation: str, ticks: list) -> pd.DataFrame:
    """ Create an Equal Weighted Portfolio
    Args:

    Returns:
        dict: Dataframe of Portfolio
    """
    portfolio = initialize_portfolio(df=df, allocation=allocation, ticks=ticks)
    # Rebalance for each date after the first one
    for date in df.index.unique()[1:]:
        print(date)
        data = df.loc[date]
        prev_portfolio = portfolio.loc[portfolio.index[-1]]
        portfolio = update_portfolio(portfolio=prev_portfolio.copy(), price_df=data, ticks=ticks, date=date)
    return portfolio

#def portfolio_value(portfolio: pd.DataFrame, price_df: pd.DataFrame) -> float:
    """ Calculates Portfolio Value

    Args:
        portfolio (pd.DataFrame): Portfolio DataFrame

    Returns:
        float: Value of Portfolio
    """
