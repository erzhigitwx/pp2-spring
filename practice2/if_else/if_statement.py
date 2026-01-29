# Example 1: Basic if
a = 33
b = 200
if b > a:
    print("b is greater than a")

# Example 2: If with multiple statements
x = 10
if x > 5:
    print("x is greater than 5")
    print("This is inside the if block")

# Example 3: If without else
score = 85
if score >= 60:
    print("You passed!")

# Example 4: Nested if
num = 15
if num > 0:
    if num % 2 == 0:
        print("Positive even number")
    if num % 2 != 0:
        print("Positive odd number")

# Example 5: If with calculation
price = 100
if price > 50:
    discount = price * 0.1
    print(f"Discount: {discount}")