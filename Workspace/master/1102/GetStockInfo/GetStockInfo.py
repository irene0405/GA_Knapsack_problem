import yfinance as yf
import os
import time

start_time = time.time()

stock_set = {'AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'GS', 'HD', 'HON',
             'IBM', 'INTC', 'JNJ', 'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',
             'PG', 'TRV', 'UNH', 'CRM', 'VZ', 'V', 'WBA', 'WMT', 'DIS', 'DOW'}

dir_name = 'DJIA_CNBC_from 2019.04.01 to 2019.05.01'

os.mkdir(dir_name)

i = 0

for stock in stock_set:
    i += 1
    print(i, end = '')
    print(':', stock)
    yf.Ticker(stock)

    df = yf.download(stock, start = '2019-4-1', end = '2019-5-1')

    df.to_csv('./' + dir_name + '/' + stock + '.csv')

print('--- Time taken: %s s ---' % (time.time() - start_time))
