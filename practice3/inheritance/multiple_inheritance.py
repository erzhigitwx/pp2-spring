# Example 1
class Flyable:
    def fly(self):
        print("Flying in the sky")


class Swimmable:
    def swim(self):
        print("Swimming in the water")


class Duck(Flyable, Swimmable):
    def __init__(self, name):
        self.name = name


duck = Duck("Donald")
print(f"{duck.name} can:")
duck.fly()
duck.swim()


# Example 2
class Person:
    def __init__(self, name):
        self.name = name
        print(f"Person: {name}")


class Employee:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        print(f"Employee ID: {employee_id}")


class Manager(Person, Employee):
    def __init__(self, name, employee_id, department):
        Person.__init__(self, name)
        Employee.__init__(self, employee_id)
        self.department = department
        print(f"Department: {department}")


print("\n--- Creating Manager ---")
manager = Manager("Alice", "E123", "IT")


# Example 3
class A:
    def process(self):
        print("Process from A")


class B(A):
    def process(self):
        print("Process from B")


class C(A):
    def process(self):
        print("Process from C")


class D(B, C):
    pass


print("\n--- Method Resolution Order ---")
d = D()
d.process()
print(f"MRO: {[cls.__name__ for cls in D.__mro__]}")


# Example 4
class Phone:
    def __init__(self):
        print("Phone initialized")

    def call(self, number):
        print(f"Calling {number}...")

    def receive_call(self):
        print("Incoming call...")


class Camera:
    def __init__(self):
        print("Camera initialized")

    def take_photo(self):
        print("📸 Photo taken")

    def record_video(self):
        print("🎥 Recording video")


class GPS:
    def __init__(self):
        print("GPS initialized")

    def get_location(self):
        return "40.7128° N, 74.0060° W"

    def navigate_to(self, destination):
        print(f"Navigating to {destination}")


class SmartPhone(Phone, Camera, GPS):
    def __init__(self, brand, model):
        Phone.__init__(self)
        Camera.__init__(self)
        GPS.__init__(self)
        self.brand = brand
        self.model = model
        print(f"Smartphone ready: {brand} {model}")


print("\n--- Creating Smartphone ---")
phone = SmartPhone("iPhone", "15 Pro")

print("\n--- Using Smartphone Features ---")
phone.call("123-456-7890")
phone.take_photo()
print(f"Location: {phone.get_location()}")
phone.navigate_to("Central Park")


# Example 5
class JSONMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)


class LogMixin:
    def log(self, message):
        print(f"[LOG] {self.__class__.__name__}: {message}")


class User(Person, JSONMixin, LogMixin):
    def __init__(self, name, email):
        Person.__init__(self, name)
        self.email = email

    def register(self):
        self.log(f"Registering user {self.name}")
        print(f"User {self.name} registered")


print("\n--- User with Mixins ---")
user = User("Bob", "bob@email.com")
user.register()
print(f"JSON: {user.to_json()}")


# Example 6
class Base:
    def __init__(self):
        print("Base init")

    def method(self):
        print("Base method")


class Left(Base):
    def __init__(self):
        super().__init__()
        print("Left init")

    def method(self):
        print("Left method")
        super().method()


class Right(Base):
    def __init__(self):
        super().__init__()
        print("Right init")

    def method(self):
        print("Right method")
        super().method()


class Diamond(Left, Right):
    def __init__(self):
        super().__init__()
        print("Diamond init")


print("\n--- Diamond Pattern ---")
diamond = Diamond()
print("\nCalling method:")
diamond.method()
print(f"\nMRO: {[cls.__name__ for cls in Diamond.__mro__]}")
