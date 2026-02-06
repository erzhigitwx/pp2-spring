# Example 1
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound")


class Dog(Animal):
    pass


dog = Dog("Buddy")
dog.speak()


# Example 2
class Cat(Animal):
    def purr(self):
        print(f"{self.name} purrs")


cat = Cat("Whiskers")
cat.speak()
cat.purr()


# Example 3
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def info(self):
        print(f"{self.brand} {self.model}")


class Car(Vehicle):
    def __init__(self, brand, model, doors):
        Vehicle.__init__(self, brand, model)
        self.doors = doors

    def full_info(self):
        print(f"{self.brand} {self.model} with {self.doors} doors")


car = Car("Toyota", "Camry", 4)
car.info()
car.full_info()


# Example 4
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hi, I'm {self.name}, {self.age} years old")


class Student(Person):
    def __init__(self, name, age, student_id):
        Person.__init__(self, name, age)
        self.student_id = student_id

    def show_id(self):
        print(f"Student ID: {self.student_id}")


class Teacher(Person):
    def __init__(self, name, age, subject):
        Person.__init__(self, name, age)
        self.subject = subject

    def teach(self):
        print(f"{self.name} teaches {self.subject}")


student = Student("Alice", 20, "S12345")
teacher = Teacher("Mr. Smith", 45, "Mathematics")

print("\n--- Student ---")
student.introduce()
student.show_id()

print("\n--- Teacher ---")
teacher.introduce()
teacher.teach()


# Example 5
class Shape:
    def __init__(self, color):
        self.color = color

    def describe(self):
        print(f"This is a {self.color} shape")


class Rectangle(Shape):
    def __init__(self, color, length, width):
        Shape.__init__(self, color)
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


class Square(Rectangle):
    def __init__(self, color, side):
        Rectangle.__init__(self, color, side, side)


square = Square("red", 5)
square.describe()
print(f"Area: {square.area()}")
