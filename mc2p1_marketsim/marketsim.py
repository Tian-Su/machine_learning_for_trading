"""
MC2-P1: Market simulator.
run script with:
PYTHONPATH=..:. ORDERS_DATA_DIR=. python grade_marketsim.py
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data


def author():
    return 'tsu35'


def calculate_leverage(trade, date, symbols):
    # initialize
    lev_abs_sum = 0
    lev_sum = 0
    # calculate the stock positions
    for tick in symbols:
        share_cum_col = str(tick + '_cum')
        stock_price_col = str(tick + '_price')
        stock_position = trade.ix[date, share_cum_col] * trade.ix[
            date, stock_price_col]
        # absolute position
        lev_abs_sum += np.abs(stock_position)
        # total position
        lev_sum += stock_position
    # cash
    cash = trade.ix[date, 'cash']
    # calculate leverage
    leverage = lev_abs_sum / (lev_sum + cash)
    return leverage


def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000,
                     transaction_cost=9.95, market_impact=0.005,
                     leverage_threshold=2.0):
    """

    Parameters
    ----------
    orders_file: the file specify the trading orders put in on specific days.
    start_val: starting cash amount of the investment.
    transaction_cost: transaction cost of each trade.
    market_impact: market fluctuation because of the trade.
    leverage_threshold: maximum threshold allowed.

    Returns
    -------
    This function return a single column data frame with portfolio value on each day.

    """
    # read in orders
    orders = pd.read_csv(orders_file, index_col=0, parse_dates=True, sep=',')
    orders = orders.sort_index()

    # get trading dates and traded stocks
    dates = pd.date_range(orders.index[0], orders.index[-1])
    dates = get_data(['SPY'], dates).index.get_values()
    symbols = orders['Symbol'].unique().tolist()

    # get price data
    prices = get_data(symbols, dates)[symbols]
    prices = pd.concat([prices, pd.DataFrame(index=dates)], axis=1)
    prices = prices.fillna(method='ffill')

    # create framework of trade table
    col = ['transaction'] + symbols
    trade = pd.DataFrame(columns=col, index=[dates])
    trade[col] = trade[col].fillna(value=0)

    # merge stock price data
    trade = trade.merge(prices, how='left', left_index=True, right_index=True,
                        suffixes=('', '_price'))

    # "execute" each order
    for i in range(len(orders)):
        # backup in case over leverage threshold
        trade_orig = trade.copy()

        # get the values of each trade
        row = orders.ix[i]
        number_share = row['Shares']
        tick = row['Symbol']
        date = orders.index[i]

        # set the buy/sell sign
        if row['Order'] == 'SELL':
            buy_sell = -1.0
        elif row['Order'] == 'BUY':
            buy_sell = 1.0
        else:
            print "Wrong value."

        # calculate the share of the stock on certain day
        trade.ix[date, tick] += (number_share * buy_sell)

        # calculate the transaction cost: stock, fee, market impact
        trade.ix[date, 'transaction'] -= prices.ix[date, tick] \
                                         * number_share \
                                         * (buy_sell + market_impact) \
                                         + transaction_cost

        # cumsum of stock shares
        trade[[str(tick + '_cum') for tick in symbols]] = trade[
            symbols].cumsum()

        # cumsum of transactions
        trade['transaction_cum'] = trade['transaction'].cumsum()

        # calculate cash in hand
        trade['cash'] = trade['transaction_cum'] + start_val

        # calculate the leverage of the trade
        leverage = calculate_leverage(trade, date, symbols)

        # prevent the transaction if over the leverage limit.
        if leverage > leverage_threshold:
            # revert back to the df before this trade
            trade = trade_orig
            print "leverage > {0}. Forbiden".format(leverage_threshold)

    # calculate stock values on each day
    trade['stock_value'] = 0
    for tick in symbols:
        trade['stock_value'] += trade[str(tick + '_cum')] * trade[
            str(tick + '_price')]

    # add the cash and stock_value to get the portfolio value
    trade['portval'] = trade['cash'] + trade['stock_value']

    return pd.DataFrame(trade['portval'])


def test_code():
    """
    This is the test frame work gaven by the instructure.
    I did not modify it, so don't think it works.
    I used the grade_marketsim.py in the same folder to test the script.
    Returns
    -------

    """
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2008, 6, 1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2, 0.01, 0.02, 1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,
                                                                           0.01,
                                                                           0.02,
                                                                           1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])


if __name__ == "__main__":
    test_code()
