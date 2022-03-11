import yfinance as yf
import os
import pandas as pd
import numpy as np
import statistics
import sys
from itertools import combinations
import time

start_y = str(2019)
start_m = str(6)
start_d = str(2)

end_y = str(2019)
end_m = str(6)
end_d = str(8)

date_dir_name = start_y + '-' + start_m + '-' + start_d + ' to ' + end_y + '-' + end_m + '-' + end_d

stock_set = {'AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'GS', 'HD', 'HON',
             'IBM', 'INTC', 'JNJ', 'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',
             'PG', 'TRV', 'UNH', 'CRM', 'VZ', 'V', 'WBA', 'WMT', 'DIS', 'DOW'}

K = 3
CRAWLER = 0


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


def GetStockInfo():
    os.mkdir(date_dir_name)

    i = 0

    for stock in stock_set:
        i += 1
        yf.Ticker(stock)

        start = start_y + '-' + start_m + '-' + start_d
        end = end_y + '-' + end_m + '-' + end_d

        df = yf.download(stock, start = start, end = end)

        df.to_csv('./' + date_dir_name + '/' + stock + '.csv')


def GetRR():
    export_dir = './datasets'
    export_file = '/attribute_result.csv'

    if os.path.exists(export_dir + export_file):
        os.remove(export_dir + export_file)
    if not os.path.exists(export_dir):
        os.mkdir(export_dir)

    export_flag = 1
    for stock in stock_set:
        df = pd.read_csv(date_dir_name + '/' + stock + '.csv')

        close_price = list(df.loc[:, 'Adj Close'])
        num_days = len(close_price)

        profit = 1.0
        for i in range(num_days - 1):
            profit *= (close_price[i + 1] / close_price[i])
        profit -= 1

        risk = np.std(close_price)

        stock_info = {'symbol': [stock[:(len(stock) - 4)]],
                      'profit': [profit],
                      'risk': [risk]
                      }

        if not export_flag:
            export_df = pd.DataFrame(stock_info)
            export_df.to_csv(export_dir + export_file, mode = 'a', index = False, header = False)
        else:
            export_df = pd.DataFrame(stock_info)
            export_df.to_csv(export_dir + export_file, mode = 'a', index = False, header = True)
            export_flag = 0


def GetAllSR():
    export_dir = './result/'
    export_file = date_dir_name + '_K=' + str(K) + '.csv'

    if os.path.exists(export_dir + export_file):
        os.remove(export_dir + export_file)
    if not os.path.exists(export_dir):
        os.mkdir(export_dir)

    f = open(export_dir + export_file, 'w')

    comb = combinations(stock_set, K)
    comb = list(comb)

    for i in range(0, K):
        f.write(str(i + 1) + ',')
    #     print(i + 1, end = ', ')
    # print('return, risk, SR')
    f.write('return,risk,SR\n')

    get_len = pd.read_csv(date_dir_name + '/AAPL.csv')
    for i in range(len(comb)):
        sum_price = np.zeros(shape = len(get_len))
        for stock in comb[i]:
            dff = pd.read_csv(date_dir_name + '/' + stock + '.csv')
            # print(stock, end = ', ')
            f.write(stock + ',')
            for i in range(len(dff)):
                price = list(dff.loc[:, 'Adj Close'])[i]
                sum_price[i] += price
        portfolio_price = sum_price / K

        sum = 0.0

        day = len(portfolio_price) - 1

        for i in range(day):
            sum += portfolio_price[i + 1] / portfolio_price[i]
            # print(sum)

        profit = (sum / day - 1) * 100
        # print(profit, end = ', ')

        dev = statistics.pstdev(portfolio_price)
        # print(dev, end = ', ')
        # print(profit / dev / 100)
        f.write(str(profit) + ',')
        f.write(str(dev) + ',')
        f.write(str(profit / dev / 100) + '\n')
    f.close()


def FindBest():
    import_dir = './result/'
    import_file = date_dir_name + '_K=' + str(K) + '.csv'

    dff = pd.read_csv(import_dir + import_file)

    max_profit_profit = sys.float_info.min
    max_profit_risk = sys.float_info.max
    max_profit_SR = sys.float_info.min
    p = []

    min_risk_profit = sys.float_info.min
    min_risk_risk = sys.float_info.max
    min_risk_SR = sys.float_info.min
    r = []

    max_SR_profit = sys.float_info.min
    max_SR_risk = sys.float_info.max
    max_SR_SR = sys.float_info.min
    s = []

    for i in range(len(dff)):
        profit = list(dff.loc[:, 'return'])[i]
        risk = list(dff.loc[:, 'risk'])[i]
        SR = list(dff.loc[:, 'SR'])[i]
        if profit > max_profit_profit:
            max_profit_profit = profit
            max_profit_risk = risk
            max_profit_SR = SR
            p.clear()
            for j in range(0, K):
                stock = list(dff.loc[:, str(j + 1)])[i]
                p.append(stock)
        if risk < min_risk_risk:
            min_risk_profit = profit
            min_risk_risk = risk
            min_risk_SR = SR
            r.clear()
            for j in range(0, K):
                stock = list(dff.loc[:, str(j + 1)])[i]
                r.append(stock)
        if SR > max_SR_SR:
            max_SR_profit = profit
            max_SR_risk = risk
            max_SR_SR = SR
            s.clear()
            for j in range(0, K):
                stock = list(dff.loc[:, str(j + 1)])[i]
                s.append(stock)

    export_dir = './result/'
    export_file = date_dir_name + '_result' + '_K=' + str(K) + '.csv'

    if os.path.exists(export_dir + export_file):
        os.remove(export_dir + export_file)
    if not os.path.exists(export_dir):
        os.mkdir(export_dir)

    f = open(export_dir + export_file, 'w')
    for i in range(0, K):
        f.write(str(i + 1) + ',')
    f.write('return,risk,SR\n')
    f.write('max profit: ')
    for i in p:
        f.write(i + ',')
    f.write(str(max_profit_profit) + ',')
    f.write(str(max_profit_risk) + ',')
    f.write(str(max_profit_SR))
    f.write('\n')

    f.write('min risk: ')
    for i in r:
        f.write(i + ',')
    f.write(str(min_risk_profit) + ',')
    f.write(str(min_risk_risk) + ',')
    f.write(str(min_risk_SR))
    f.write('\n')

    f.write('max SR: ')
    for i in s:
        f.write(i + ',')
    f.write(str(max_SR_profit) + ',')
    f.write(str(max_SR_risk) + ',')
    f.write(str(max_SR_SR))
    f.close()


if __name__ == '__main__':
    start_time = time.time()
    if CRAWLER:
        GetStockInfo()
    GetRR()
    GetAllSR()
    FindBest()

    print('\n--- Time taken: %s s ---' % (time.time() - start_time))

    export_dir = './result/'
    export_file = date_dir_name + '_result' + '_K=' + str(K) + '.csv'

    f = open(export_dir + export_file, 'a')
    f.write('\n\n--- Time taken: ' + str(time.time() - start_time) + ' s ---')
    f.close()
