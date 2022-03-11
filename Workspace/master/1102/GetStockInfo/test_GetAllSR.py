import pandas as pd
import numpy as np
import statistics
from itertools import combinations
import time

K = 2
PROCESSING = 1

date_dir_name = './DJIA_CNBC_from 2019-4-1 to 2019-5-1/'

class Stocks:
    def __init__(self, symbol, profit, risk):
        self.symbol = symbol
        self.profit = profit
        self.risk = risk

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_profit(self, profit):
        self.profit = profit

    def set_risk(self, risk):
        self.risk = risk


def get_stock():
    df = pd.read_csv('datasets/attribute_result.csv')
    symbols = list(df.loc[:, 'symbol'])
    return symbols


def make_combinations(symbols):
    comb = combinations(symbols, K)
    comb = list(comb)
    # print(comb)
    return comb


def get_portfolio(comb):
    # print(len(comb)) # 435 combinations
    for i in range(len(comb)):
        get_len = pd.read_csv(date_dir_name + 'AAPL.csv')
        sum_price = np.zeros(shape = len(get_len))
        for stock in comb[i]:
            # print(stock)
            # print(len(get_len))
            dff = pd.read_csv(date_dir_name + stock + '.csv')
            # print(stock, end = ',')
            for i in range(len(dff)):
                price = list(dff.loc[:, 'Adj Close'])[i]
                sum_price[i] += price
        portfolio_price = sum_price / 2

        sum = 0.0

        day = len(portfolio_price) - 1

        for i in range(day):
            sum += portfolio_price[i + 1] / portfolio_price[i]
            # print(sum)

        profit = (sum / day - 1) * 100
        # print('\nreturn:', profit, end = '')
        # print(' %')

        dev = statistics.pstdev(portfolio_price)
        # print('   dev:', dev)
        print('    SR:', profit / dev / 100)
        # print('--------------------------------------')


if __name__ == '__main__':
    start_time = time.time()
    symbols = get_stock()
    N = len(symbols)

    comb = make_combinations(symbols)
    get_portfolio(comb)
    #
    # g_skyline = check(stocks, comb)
    #
    # run_time = time.time() - start_time
    # export(run_time, N, K, g_skyline)
    print('--- Time taken: %s s ---' % (time.time() - start_time))
