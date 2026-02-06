# Example 1
def add(x, y):
    return x + y

add_lambda = lambda x, y: x + y

print(f"Regular function: {add(5, 3)}")
print(f"Lambda function: {add_lambda(5, 3)}")

# Example 2
square = lambda x: x ** 2
cube = lambda x: x ** 3

print(f"Square of 5: {square(5)}")
print(f"Cube of 3: {cube(3)}")

# Example 3
is_even = lambda x: "Even" if x % 2 == 0 else "Odd"

print(f"4 is {is_even(4)}")
print(f"7 is {is_even(7)}")

# Example 4
full_name = lambda first, last: f"{first} {last}"
reverse_string = lambda s: s[::-1]

print(full_name("John", "Doe"))
print(f"Reverse of 'Python': {reverse_string('Python')}")

# Example 5
result = (lambda x, y: x * y)(5, 4)
print(f"5 * 4 = {result}")

factorial = (lambda n: 1 if n == 0 else n * factorial(n - 1))

# Example 6
operations = [
    lambda x: x + 10,
    lambda x: x * 2,
    lambda x: x ** 2
]

number = 5
print(f"\nApplying operations to {number}:")
for i, operation in enumerate(operations, 1):
    print(f"Operation {i}: {operation(number)}")

# Example 7
celsius_to_fahrenheit = lambda c: (c * 9/5) + 32
fahrenheit_to_celsius = lambda f: (f - 32) * 5/9

temp_c = 25
temp_f = 77
print(f"\n{temp_c}°C = {celsius_to_fahrenheit(temp_c)}°F")
print(f"{temp_f}°F = {fahrenheit_to_celsius(temp_f):.1f}°C")