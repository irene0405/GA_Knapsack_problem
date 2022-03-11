import pandas as pd
import numpy as np
import time
import statistics

date_dir_name = './DJIA_CNBC_from 2019-4-1 to 2019-5-1/'

class Stocks:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_price(self, price):
        self.price = price


def get_portfolio():
    df = pd.read_csv('FGSB_result/G_Skyline_2.csv')
    print(df)
    for i in range(len(df)):
        tmplist = eval(list(df.loc[:, 'Portfolio'])[i])

        get_len = pd.read_csv(date_dir_name + tmplist[0] + '.csv')

        sum_price = np.zeros(shape = len(get_len))
        for stock in tmplist:
            dff = pd.read_csv(date_dir_name + stock + '.csv')
            print(stock, end = ',')
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
        print('\nreturn:', profit, end = '')
        print(' %')

        dev = statistics.pstdev(portfolio_price)
        print('   dev:', dev)
        print('    SR:', profit / dev / 100)
        print('--------------------------------------')


if __name__ == '__main__':
    start_time = time.time()
    get_portfolio()

    run_time = time.time() - start_time
    print('\n\n--- Time taken: %s s ---' % (time.time() - start_time))
