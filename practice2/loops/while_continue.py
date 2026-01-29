# Example 1: Skip specific value
i = 0
while i < 6:
    i += 1
    if i == 3:
        continue
    print(i)

# Example 2: Print only even numbers
num = 0
while num < 10:
    num += 1
    if num % 2 != 0:
        continue
    print(num)

# Example 3: Skip negative numbers
numbers = [-2, -1, 0, 1, 2, 3]
i = 0
while i < len(numbers):
    if numbers[i] < 0:
        i += 1
        continue
    print(numbers[i])
    i += 1

# Example 4: Skip multiples of 3
count = 0
while count < 15:
    count += 1
    if count % 3 == 0:
        continue
    print(count)

# Example 5: Process valid data only
data = [10, -5, 20, 0, 30, -10, 40]
i = 0
while i < len(data):
    value = data[i]
    i += 1
    if value <= 0:
        continue
    print(f"Processing: {value}")