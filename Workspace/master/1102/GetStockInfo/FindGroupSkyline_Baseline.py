import pandas as pd
import csv
from itertools import permutations
import time
import os

K = 2
PROCESSING = 1


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
    stocks = []
    df = pd.read_csv('datasets/attribute_result.csv')
    for i in range(len(df)):
        symbol = list(df.loc[:, 'symbol'])[i]
        profit = list(df.loc[:, 'profit'])[i]
        risk = list(df.loc[:, 'risk'])[i]
        s = Stocks(symbol, profit, risk)
        stocks.append(s)

    symbols = list(df.loc[:, 'symbol'])
    return stocks, symbols


def make_combinations(symbols):
    comb = permutations(symbols, K)
    comb = list(comb)
    return comb


def cmp_list(stocks, list_1, list_2):
    num_stock = len(stocks)
    len_comb = len(list_1)
    profit_1 = []
    profit_2 = []
    risk_1 = []
    risk_2 = []
    for j in range(len_comb):
        for i in range(num_stock):
            if stocks[i].symbol == list_1[j]:
                profit_1.append(stocks[i].profit)
                risk_1.append(stocks[i].risk)

            if stocks[i].symbol == list_2[j]:
                profit_2.append(stocks[i].profit)
                risk_2.append(stocks[i].risk)

    for i in range(len_comb):
        if profit_1[i] < profit_2[i] or risk_1[i] > risk_2[i]:
            return False

    return True


def check(stocks, comb):
    non_skyline_list = []
    for i in range(0, len(comb), 1):
        if PROCESSING:
            if i % 10 == 0:
                print(i, '/', len(comb))
        for j in range(0, len(comb), 1):

            if i != j and (i not in non_skyline_list) and (j not in non_skyline_list):
                result = cmp_list(stocks, comb[i], comb[j])
                if result is True:
                    non_skyline_list.append(j)

    non_skyline_list.sort()
    result_list = []
    for element in non_skyline_list:
        if element not in result_list:
            result_list.append(element)
    result_list.reverse()
    for i in range(len(result_list)):
        if comb[result_list[i]] in comb:
            comb.remove(comb[result_list[i]])
            # print(comb)
    comb = list(set(frozenset(e) for e in comb))
    solution = [list(x) for x in comb]
    return solution


def export(run_time, N, K, g_skyline):
    # w.writerow(['N = ' + str(N)])
    # w.writerow(['K = ' + str(K)])
    w.writerow(['Portfolio'])
    for i in range(len(g_skyline)):
        w.writerow([g_skyline[i]])
    # w.writerow([])
    # w.writerow(['--- Time taken: %s s ---' % run_time])


if __name__ == '__main__':
    start_time = time.time()
    stocks, symbols = get_stock()
    N = len(symbols)

    export_dir = 'FGSB_result'
    export_file = '/G_Skyline_' + str(K) + '.csv'
    if not os.path.exists(export_dir):
        os.mkdir(export_dir)
    if os.path.exists(export_dir + export_file):
        os.remove(export_dir + export_file)
    with open(export_dir + export_file, 'a', newline = '') as csvfile:
        w = csv.writer(csvfile)
        comb = make_combinations(symbols)

        g_skyline = check(stocks, comb)

        run_time = time.time() - start_time
        export(run_time, N, K, g_skyline)
    print('--- Time taken: %s s ---' % (time.time() - start_time))
