""" Import stock level data
"""
import yfinance as yf
import pandas as pd

def pull_stock_data(tickers:list, start:str, end:str) -> pd.DataFrame:
    """_summary_

    Args:
        tickers (list): Ticker(s) to imprt data for
        start (str): Date Format: %Y-%m-%d
        end (str): Date Format: %Y-%m-%d

    Returns:
        pd.DataFrame: dataframe of stock data
    """
    df = yf.download(tickers=tickers, start=start, end=end)
    return df

def one_stock_data(dataframe: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """ Return dataframe with one ticker

    Args:
        dataframe (pd.DataFrame): Dataframe of Multiple Tickers
        ticker (str): Stock Ticker

    Returns:
        pd.DataFrame: Dataframe with Single Ticker
    """
    return dataframe.loc[:, (slice(None), ticker)]
