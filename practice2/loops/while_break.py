# Example 1: Break when condition met
i = 1
while i < 6:
    print(i)
    if i == 3:
        break
    i += 1

# Example 2: Search in loop
target = 7
num = 1
while num <= 10:
    if num == target:
        print(f"Found {target}!")
        break
    num += 1

# Example 3: Break on specific condition
count = 0
while True:
    print(count)
    count += 1
    if count >= 5:
        break

# Example 4: Password attempt with break
attempts = 0
while attempts < 5:
    attempts += 1
    if attempts == 3:
        print("Correct password!")
        break
    print(f"Attempt {attempts}: Wrong password")

# Example 5: Finding first even number
numbers = [1, 3, 5, 8, 9, 10]
i = 0
while i < len(numbers):
    if numbers[i] % 2 == 0:
        print(f"First even number: {numbers[i]}")
        break
    i += 1