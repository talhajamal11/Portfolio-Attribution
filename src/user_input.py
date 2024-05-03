""" Script to get user input
"""
import re

def get_tickers() -> str:
    """ Request user for Tickers

    Returns:
        list: List of Tickers
    """
    while True:
        try:
            tickers = input("Please enter all Tickers requested for the Portfolio, separated by one space between each of them:")
            if not isinstance(tickers, str):
                raise ValueError("Invalid input: tickers must be strings.")
            # Split on spaces into a list, strip numeric characters and capitalize each ticker
            tickers = tickers.split()
            result = [re.sub(r'\d+', '', word).upper() for word in tickers]
            return result
        except ValueError as e:
            print(e)

def get_portfolio_allocation() -> int:
    """ Request user for integer dollar amount to allocate to portfolio

    Returns:
        int: Portfolio Starting Networth
    """
    while True:
        try:
            allocation = int(input("Please enter an integer amount for starting Portfolio Net Worth:"))
            if allocation < 0:
                raise ValueError("The allocated amount must be a positive")
            return allocation
        except ValueError as e:
            print(e)
