# Example 1
def greet():
    print("Hello, World!")
    print("Welcome to Python functions!")

greet()

# Example 2
def greet_person(name):
    print(f"Hello, {name}!")
    print(f"Nice to meet you, {name}")

greet_person("Alice")
greet_person("Bob")

# Example 3
def introduce(name, age, city):
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"City: {city}")

introduce("John", 25, "New York")

# Example 4
def calculate_area(length, width):
    area = length * width
    print(f"Rectangle {length}x{width}")
    print(f"Area: {area}")

calculate_area(5, 3)
calculate_area(10, 7)

# Example 5
def check_eligibility(age):
    if age >= 18:
        print(f"Age {age}: Eligible to vote")
    else:
        print(f"Age {age}: Not eligible to vote")

check_eligibility(20)
check_eligibility(16)