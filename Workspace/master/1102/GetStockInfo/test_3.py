import pandas as pd
import sys

K = 2

start_y = str(2019)
start_m = str(6)
start_d = str(2)

end_y = str(2019)
end_m = str(6)
end_d = str(8)

date_dir_name = 'DJIA_CNBC_from ' + start_y + '-' + start_m + '-' + start_d + ' to ' + end_y + '-' + end_m + '-' + end_d
export_dir = './result/'
export_file = date_dir_name + '.csv'

dff = pd.read_csv(export_dir + export_file)

max_profit = sys.float_info.min
min_risk = sys.float_info.max
max_SR = sys.float_info.min

p = []
r = []
s = []

for i in range(len(dff)):
    # stock_A = list(dff.loc[:, A])[i]
    # stock_B = list(dff.loc[:, B])[i]
    profit = list(dff.loc[:, 'return'])[i]
    risk = list(dff.loc[:, 'risk'])[i]
    SR = list(dff.loc[:, 'SR'])[i]
    if profit > max_profit:
        max_profit = profit
        p.clear()
        for j in range(0, K):
            stock = list(dff.loc[:, str(j + 1)])[i]
            p.append(stock)
    if risk < min_risk:
        min_risk = risk
        r.clear()
        for j in range(0, K):
            stock = list(dff.loc[:, str(j + 1)])[i]
            r.append(stock)
    if SR > max_SR:
        max_SR = SR
        s.clear()
        for j in range(0, K):
            stock = list(dff.loc[:, str(j + 1)])[i]
            s.append(stock)

print(p, max_profit)
print(r, min_risk)
print(s, max_SR)