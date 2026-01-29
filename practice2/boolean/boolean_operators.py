# Example 1: AND operator
x = 5
print(x > 3 and x < 10)
print(x > 3 and x > 10)

# Example 2: OR operator
x = 5
print(x > 3 or x < 4)
print(x < 3 or x < 4)

# Example 3: NOT operator
x = 5
print(not(x > 3 and x < 10))
print(not(x < 3))

# Example 4: Combining operators
a = 10
b = 5
c = 15
print(a > b and b < c)
print(a > b or a > c)
print(not(a < b))

# Example 5: Complex boolean expressions
age = 25
has_license = True
print(age >= 18 and has_license)
print(age < 18 or not has_license)