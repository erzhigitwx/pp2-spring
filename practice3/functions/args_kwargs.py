# Example 1
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total


print(sum_all(1, 2, 3))  # 6
print(sum_all(5, 10, 15, 20))  # 50
print(sum_all(1, 2, 3, 4, 5, 6))  # 21


# Example 2
def make_sandwich(size, *ingredients):
    print(f"\nMaking a {size}-inch sandwich with:")
    for ingredient in ingredients:
        print(f"  - {ingredient}")


make_sandwich(6, "cheese", "tomato")
make_sandwich(12, "ham", "cheese", "lettuce", "tomato", "onion")


# Example 3
def print_user_info(**info):
    print("\nUser Information:")
    for key, value in info.items():
        print(f"{key}: {value}")


print_user_info(name="Alice", age=25, city="London")
print_user_info(name="Bob", age=30, city="Paris", job="Engineer", hobby="Reading")


# Example 4
def create_profile(name, *skills, **details):
    print(f"\n=== Profile: {name} ===")

    if skills:
        print("Skills:")
        for skill in skills:
            print(f"  - {skill}")

    if details:
        print("Details:")
        for key, value in details.items():
            print(f"  {key}: {value}")


create_profile("Alice", "Python", "JavaScript", age=25, city="London")
create_profile("Bob", "Java", "C++", "SQL", age=30, experience=5)


# Example 5
def calculate(operation, *numbers, **options):
    result = 0

    if operation == "sum":
        result = sum(numbers)
    elif operation == "multiply":
        result = 1
        for num in numbers:
            result *= num
    elif operation == "average":
        result = sum(numbers) / len(numbers)

    if options.get("round"):
        result = round(result, options.get("decimals", 2))

    print(f"Operation: {operation}")
    print(f"Numbers: {numbers}")
    print(f"Result: {result}")
    return result


calculate("sum", 1, 2, 3, 4, 5)
calculate("multiply", 2, 3, 4)
calculate("average", 10, 20, 30, round=True, decimals=1)


# Example 6
def demo_unpacking(*args, **kwargs):
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")


numbers = [1, 2, 3]
demo_unpacking(*numbers)

info = {"name": "Alice", "age": 25}
demo_unpacking(**info)