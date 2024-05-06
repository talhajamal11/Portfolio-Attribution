""" 
    Script to calculate Portfolio Metrics
"""
import pandas as pd

def portfolio_value(portfolio: pd.DataFrame) -> pd.Series:
    """ Caculate Portfolio Value at each date

    Args:
        portfolio (pd.DataFrame): Portfolio DataFrame

    Returns:
        pd.Series: Series with the Value of the Portfolio on Each Date
    """
    return portfolio.groupby(['Date'])['Total Value'].sum()

def portfolio_returns(pf_value: pd.DataFrame) -> pd.Series:
    """ Calculate Returns of the Portfolio

    Args:
        portfolio_value (pd.DataFrame): Portfolio Value at each holding frquency

    Returns:
        pd.Series: Return a Series of Portfolio Returns
    """
    return pf_value.pct_change().dropna()
