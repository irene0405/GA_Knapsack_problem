price = [2.0, 4.0, 3.0, 5.0, 4.0, 6.0]

sum = 1.0

day = len(price) - 1

for i in range(day):
    sum *= price[i + 1] / price[i]
    print(price[i + 1], end = '')
    print('/', end = '')
    print(price[i])
    print(sum)

sum -= 1

print()
print(sum)

# should return 2.0