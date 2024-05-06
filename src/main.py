""" Portfolio Attribution Project
"""
from eq_weighted_portfolio import create_portfolio
from user_input import get_tickers
from user_input import get_portfolio_allocation
from pull_data import pull_stock_data
from portfolio_metrics import portfolio_value
from portfolio_metrics import portfolio_returns
from portfolio_metrics import portfolio_volatility

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
                               start="2024-01-15",
                                end="2024-01-20")
 
    # Create Portfolio
    portfolio = create_portfolio(price_df=price_df, allocation=allocation, ticks=ticks)
    print(portfolio)

    # Calculate Portfolio Metrics
    pf_value = portfolio_value(portfolio=portfolio)
    print(pf_value)

    # Caculate Portfolio Returns
    pf_ret = portfolio_returns(pf_value=pf_value)
    print(pf_ret)

    # Calculate Portfolio Volatility
    pf_vol = portfolio_volatility(pf_ret=pf_ret)
    print(pf_vol)
    
    return None

if __name__== "__main__":
    main()
