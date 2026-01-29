# Example 1: Basic while loop
i = 1
while i < 6:
    print(i)
    i += 1

# Example 2: While with condition
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1

# Example 3: While with user-like input simulation
password = ""
attempts = 0
while password != "secret" and attempts < 3:
    password = "wrong" if attempts < 2 else "secret"
    attempts += 1
    print(f"Attempt {attempts}")

# Example 4: Countdown
n = 5
while n > 0:
    print(n)
    n -= 1
print("Blast off!")

# Example 5: Sum numbers
total = 0
num = 1
while num <= 10:
    total += num
    num += 1
print(f"Sum: {total}")