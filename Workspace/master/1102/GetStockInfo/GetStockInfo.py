import yfinance as yf
import os
import time

start_time = time.time()

stock_set = {'AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'GS', 'HD', 'HON',
             'IBM', 'INTC', 'JNJ', 'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE',
             'PG', 'TRV', 'UNH', 'CRM', 'VZ', 'V', 'WBA', 'WMT', 'DIS', 'DOW'}

start_y = str(2019)
start_m = str(6)
start_d = str(2)

end_y = str(2020)
end_m = str(7)
end_d = str(1)

date_dir_name = 'DJIA_CNBC_from ' + start_y + '-' + start_m + '-' + start_d + ' to ' + end_y + '-' + end_m + '-' + end_d

os.mkdir(date_dir_name)

i = 0

for stock in stock_set:
    i += 1
    # print(i, end = '')
    # print(':', stock)
    yf.Ticker(stock)

    start = start_y + '-' + start_m + '-' + start_d
    end = end_y + '-' + end_m + '-' + end_d

    df = yf.download(stock, start = start, end = end)

    df.to_csv('./' + date_dir_name + '/' + stock + '.csv')

print('from ' + start_y + '-' + start_m + '-' + start_d + ' to ' + end_y + '-' + end_m + '-' + end_d)
print('--- Time taken: %s s ---' % (time.time() - start_time))
