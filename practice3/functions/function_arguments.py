# Example 1
def describe_pet(animal_type, pet_name):
    print(f"I have a {animal_type}.")
    print(f"My {animal_type}'s name is {pet_name}.")

describe_pet("dog", "Rex")
describe_pet("cat", "Whiskers")

# Example 2
def describe_person(name, age, city):
    print(f"{name} is {age} years old and lives in {city}")

describe_person(age=25, city="London", name="Alice")
describe_person(name="Bob", age=30, city="Paris")

# Example 3
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")
greet("Bob", "Hi")
greet("Charlie", greeting="Hey")

# Example 4
def order_pizza(size, *toppings, delivery=False):
    print(f"\nOrdering a {size}-inch pizza")
    print("Toppings:")
    for topping in toppings:
        print(f"  - {topping}")
    if delivery:
        print("Delivery: Yes")
    else:
        print("Pickup: Yes")

order_pizza(12, "mushrooms", "pepperoni")
order_pizza(16, "olives", "cheese", "tomatoes", delivery=True)

# Example 5
def calculate_discount(price, discount_percent=10, member=False):
    discount = price * (discount_percent / 100)
    if member:
        discount += price * 0.05  # дополнительные 5% для членов
    final_price = price - discount
    print(f"Original price: ${price}")
    print(f"Discount: ${discount:.2f}")
    print(f"Final price: ${final_price:.2f}")

calculate_discount(100)
calculate_discount(100, 20)
calculate_discount(100, 15, member=True)