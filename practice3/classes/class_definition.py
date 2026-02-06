# Example 1
class Dog:
    pass


my_dog = Dog()
print(f"Created object: {my_dog}")
print(f"Type: {type(my_dog)}")


# Example 2
class Person:
    name = "Unknown"
    age = 0


person1 = Person()
person1.name = "Alice"
person1.age = 25

print(f"\nPerson: {person1.name}, {person1.age} years old")


# Example 3
class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


calc = Calculator()
print(f"\n5 + 3 = {calc.add(5, 3)}")
print(f"5 * 3 = {calc.multiply(5, 3)}")


# Example 4
class Rectangle:
    def set_dimensions(self, length, width):
        self.length = length
        self.width = width

    def get_area(self):
        return self.length * self.width

    def get_perimeter(self):
        return 2 * (self.length + self.width)


rect = Rectangle()
rect.set_dimensions(5, 3)
print(f"\nRectangle {rect.length}x{rect.width}")
print(f"Area: {rect.get_area()}")
print(f"Perimeter: {rect.get_perimeter()}")


# Example 5
class Car:
    def set_info(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        print(f"{self.year} {self.make} {self.model}")


car1 = Car()
car1.set_info("Toyota", "Camry", 2020)

car2 = Car()
car2.set_info("Honda", "Civic", 2021)

print("\nCar 1:")
car1.display_info()

print("Car 2:")
car2.display_info()