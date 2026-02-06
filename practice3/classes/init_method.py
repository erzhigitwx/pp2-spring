# Example 1
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hi, I'm {self.name} and I'm {self.age} years old")


person1 = Person("Alice", 25)
person1.introduce()

person2 = Person("Bob", 30)
person2.introduce()


# Example 2
class Student:
    def __init__(self, name, grade="A", school="Unknown"):
        self.name = name
        self.grade = grade
        self.school = school

    def display(self):
        print(f"Student: {self.name}")
        print(f"Grade: {self.grade}")
        print(f"School: {self.school}")


student1 = Student("Charlie", "B", "MIT")
print("\nStudent 1:")
student1.display()

student2 = Student("David")
print("\nStudent 2:")
student2.display()


# Example 3
class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.balance = initial_balance
        print(f"Account created for {owner} with ${initial_balance}")

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited ${amount}. New balance: ${self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("Insufficient funds!")


print("\n--- Bank Account Demo ---")
account = BankAccount("Alice", 1000)
account.deposit(500)
account.withdraw(200)
account.withdraw(2000)


# Example 4
class Rectangle:
    def __init__(self, length, width):
        if length <= 0 or width <= 0:
            raise ValueError("Dimensions must be positive")
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


print("\n--- Rectangle Demo ---")
rect1 = Rectangle(5, 3)
print(f"Rectangle: {rect1.length}x{rect1.width}, Area: {rect1.area()}")


# Example 5
class Employee:
    company = "TechCorp"

    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary
        self.hire_date = "2024-01-01"

    def give_raise(self, amount):
        self.salary += amount
        print(f"{self.name}'s new salary: ${self.salary}")

    def info(self):
        print(f"\nEmployee: {self.name}")
        print(f"Position: {self.position}")
        print(f"Salary: ${self.salary}")
        print(f"Company: {self.company}")


emp1 = Employee("Alice", "Developer", 80000)
emp1.info()
emp1.give_raise(10000)