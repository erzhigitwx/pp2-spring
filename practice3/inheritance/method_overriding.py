# Example 1
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"


class Dog(Animal):
    def speak(self):
        return f"{self.name} barks: Woof!"


class Cat(Animal):
    def speak(self):
        return f"{self.name} meows: Meow!"


animals = [Dog("Buddy"), Cat("Whiskers"), Animal("Generic")]
print("--- Animals Speaking ---")
for animal in animals:
    print(animal.speak())


# Example 2
class Shape:
    def __init__(self, color):
        self.color = color

    def area(self):
        return 0

    def describe(self):
        return f"A {self.color} shape with area {self.area()}"


class Rectangle(Shape):
    def __init__(self, color, length, width):
        super().__init__(color)
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2


rect = Rectangle("blue", 5, 3)
circle = Circle("red", 4)

print(f"\n{rect.describe()}")
print(f"{circle.describe()}")


# Example 3
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} years old"

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


person = Person("Alice", 25)
print(f"\nprint(): {person}")
print(f"repr(): {repr(person)}")


# Example 4
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_bonus(self):
        return self.salary * 0.1

    def total_compensation(self):
        return self.salary + self.calculate_bonus()


class Manager(Employee):
    def calculate_bonus(self):
        return self.salary * 0.2


class Executive(Manager):
    def calculate_bonus(self):
        base_bonus = super().calculate_bonus()
        return base_bonus + 10000


employees = [
    Employee("Bob", 50000),
    Manager("Alice", 80000),
    Executive("Charlie", 120000)
]

print("\n--- Employee Compensation ---")
for emp in employees:
    print(
        f"{emp.name}: Salary=${emp.salary}, "
        f"Bonus=${emp.calculate_bonus():.2f}, "
        f"Total=${emp.total_compensation():.2f}"
    )


# Example 5
class PaymentMethod:
    def process_payment(self, amount):
        raise NotImplementedError("Subclass must implement this method")


class CreditCard(PaymentMethod):
    def process_payment(self, amount):
        print(f"Processing ${amount} via Credit Card")
        print("Card charged successfully")


class PayPal(PaymentMethod):
    def process_payment(self, amount):
        print(f"Processing ${amount} via PayPal")
        print("PayPal payment completed")


class Cash(PaymentMethod):
    def process_payment(self, amount):
        print(f"Received ${amount} in cash")
        print("Change returned")


payments = [CreditCard(), PayPal(), Cash()]
amount = 100

print("\n--- Processing Payments ---")
for i, payment_method in enumerate(payments, 1):
    print(f"\nPayment {i}:")
    payment_method.process_payment(amount)
