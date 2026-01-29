# Example 1: Break when value found
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
    if fruit == "banana":
        break

# Example 2: Break at specific number
for i in range(10):
    if i == 5:
        break
    print(i)

# Example 3: Search and break
numbers = [1, 3, 5, 7, 8, 9]
for num in numbers:
    if num % 2 == 0:
        print(f"Found even number: {num}")
        break

# Example 4: Break on condition
for i in range(1, 100):
    if i * i > 50:
        print(f"First number whose square > 50: {i}")
        break

# Example 5: Break in nested loop
for i in range(3):
    for j in range(3):
        if i == j == 1:
            break
        print(f"i={i}, j={j}")