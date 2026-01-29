a = 2
b = 330

# Example 1: Short hand if
if a > b: print("a is greater than b")

# Example 2: Short hand if-else (ternary operator)
print("A") if a > b else print("B")

# Example 3: Ternary with variable assignment
age = 20
status = "Adult" if age >= 18 else "Minor"
print(status)

# Example 4: Multiple conditions in ternary
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")

# Example 5: Ternary in calculations
x = 10
result = x * 2 if x > 5 else x + 2
print(result)