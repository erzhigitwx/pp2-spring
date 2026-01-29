# Example 1: Skip specific value
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    if fruit == "banana":
        continue
    print(fruit)

# Example 2: Skip odd numbers
for i in range(10):
    if i % 2 != 0:
        continue
    print(i)

# Example 3: Skip negative numbers
numbers = [-2, 3, -1, 5, -4, 8]
for num in numbers:
    if num < 0:
        continue
    print(num)

# Example 4: Skip multiples of 3
for i in range(1, 20):
    if i % 3 == 0:
        continue
    print(i)

# Example 5: Process valid strings only
words = ["hello", "", "world", "", "python"]
for word in words:
    if word == "":
        continue
    print(word.upper())