import statistics

price = [123.6956635,
123.3767064,
123.026329,
124.2674688,
125.0139465,
125.1885961,
125.1063436,
124.9145762,
125.1659622,
128.2974319,
128.9113744,
128.7730967,
129.1326192,
131.1813558,
131.2578074,
132.9659373,
132.2989375,
132.6212285,
133.8477376,
133.9162216,
134.161588]

sum = 0.0

day = len(price) - 1

for i in range(day):
    sum += price[i + 1] / price[i]
    # print(sum)

profit = (sum / day - 1) * 100
print(profit, end = ', ')

dev = statistics.pstdev(price)
print(dev, end = ', ')
print(profit / dev / 100)