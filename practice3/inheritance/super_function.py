# Example 1
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f"Animal created: {name}")

    def speak(self):
        print(f"{self.name} makes a sound")


class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
        print(f"Dog breed: {breed}")

    def speak(self):
        super().speak()
        print(f"{self.name} barks!")


dog = Dog("Buddy", 3, "Labrador")
dog.speak()


# Example 2
class Vehicle:
    def __init__(self, brand):
        self.brand = brand
        print(f"Vehicle: {brand}")

    def start(self):
        print(f"{self.brand} engine starting...")


class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model
        print(f"Car model: {model}")

    def start(self):
        super().start()
        print(f"{self.model} ready to drive")


class ElectricCar(Car):
    def __init__(self, brand, model, battery_capacity):
        super().__init__(brand, model)
        self.battery_capacity = battery_capacity
        print(f"Battery: {battery_capacity} kWh")

    def start(self):
        print("Checking battery...")
        super().start()
        print("Electric motor activated")


print("\n--- Creating Electric Car ---")
tesla = ElectricCar("Tesla", "Model S", 100)
print("\n--- Starting Electric Car ---")
tesla.start()


# Example 3
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Salary: ${self.salary}")


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def display_info(self):
        super().display_info()
        print(f"Team size: {self.team_size}")


print("\n--- Manager Info ---")
manager = Manager("Alice", 90000, 5)
manager.display_info()


# Example 4
class A:
    def __init__(self):
        print("A init")

    def method(self):
        print("Method from A")


class B(A):
    def __init__(self):
        print("B init")
        super().__init__()

    def method(self):
        print("Method from B")
        super().method()


class C(A):
    def __init__(self):
        print("C init")
        super().__init__()

    def method(self):
        print("Method from C")
        super().method()


class D(B, C):
    def __init__(self):
        print("D init")
        super().__init__()

    def method(self):
        print("Method from D")
        super().method()


print("\n--- Multiple Inheritance with super() ---")
d = D()
print("\n--- Method Resolution Order ---")
d.method()


# Example 5
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited ${amount}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}")
        else:
            print("Insufficient funds")


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, interest_rate=0.02):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        super().deposit(interest)
        print(f"Interest added: ${interest:.2f}")


print("\n--- Savings Account ---")
account = SavingsAccount("Bob", 1000)
account.add_interest()
