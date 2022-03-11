import statistics

portfolio_price = [82.82862282, 83.05284882, 83.58636856, 83.22631836, 83.51537132, 83.6636734, 83.20597649, 83.94161224,
                   83.90814781, 84.52628517, 84.69907188, 84.74296379, 84.93284035, 85.74957275, 85.91092873, 86.88614655,
                   86.76527023, 88.51809502, 88.66946411, 88.72643089, 89.04574394]

# price = [2.0, 4.0, 3.0, 5.0, 4.0, 6.0]

sum = 0.0

day = len(portfolio_price) - 1

for i in range(day):
    sum += portfolio_price[i + 1] / portfolio_price[i]
    # print(sum)

profit = (sum / day - 1) * 100
print('return: ', profit, end = '')
print(' %')

dev = statistics.pstdev(portfolio_price)
print('dev: ', dev)
print('SR: ', profit / dev / 100)

# output
# return:  0.36412704681614283 %
# dev:  2.029298512816969
# SR:  0.0017943493503608798