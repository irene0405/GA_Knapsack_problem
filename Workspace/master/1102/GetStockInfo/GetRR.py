import pandas as pd
import numpy as np
import time
import os

dir_name = './DJIA_CNBC_from 2019.04.01 to 2019.05.01/'

DJIA = []

for filename in os.listdir(dir_name):
    if filename != '.DS_Store':
        DJIA.append(filename)
    # print(DJIA)


def make_datasets(export_dir, export_file):
    export_flag = 1
    for stock in DJIA:
        print(stock)
        df = pd.read_csv(dir_name + stock)

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


if __name__ == '__main__':
    start_time = time.time()
    export_dir = './datasets'
    export_file = '/attribute_result.csv'
    if os.path.exists(export_dir + export_file):
        os.remove(export_dir + export_file)
    if not os.path.exists(export_dir):
        os.mkdir(export_dir)

    make_datasets(export_dir, export_file)
    print('--- Time taken: %s s ---' % (time.time() - start_time))
