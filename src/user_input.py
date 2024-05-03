""" Script to get user input
"""
import re
import yfinance

def get_tickers() -> str:
    """ Request user for Tickers

    Returns:
        list: List of Tickers
    """
    print("Please enter all Tickers requested for the Portfolio, \
          separated by one space between each of them")
    tickers = input()
    # Split on spaces into a list
    tickers = tickers.split()
    # Strip numeric characters and capitalize each ticker
    result = [re.sub(r'\d+', '', word).upper() for word in tickers]
    return result

