# Example 1
class Dog:
    species = "Canis familiaris"
    def __init__(self, name, age):
        self.name = name
        self.age = age


dog1 = Dog("Buddy", 3)
dog2 = Dog("Lucy", 5)

print(f"dog1: {dog1.name}, {dog1.age}, {dog1.species}")
print(f"dog2: {dog2.name}, {dog2.age}, {dog2.species}")

Dog.species = "Dog"
print(f"\nAfter changing class variable:")
print(f"dog1 species: {dog1.species}")
print(f"dog2 species: {dog2.species}")


# Example 2
class Employee:
    count = 0
    company = "TechCorp"

    def __init__(self, name, position):
        self.name = name
        self.position = position
        Employee.count += 1
        self.employee_id = Employee.count

    def display(self):
        print(f"ID: {self.employee_id}")
        print(f"Name: {self.name}")
        print(f"Position: {self.position}")
        print(f"Company: {self.company}")


emp1 = Employee("Alice", "Developer")
emp2 = Employee("Bob", "Designer")
emp3 = Employee("Charlie", "Manager")

print(f"\nTotal employees: {Employee.count}")
print("\nEmployee 1:")
emp1.display()
print("\nEmployee 2:")
emp2.display()

# Example 3
class Product:
    tax_rate = 0.1

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_total_price(self):
        return self.price * (1 + self.tax_rate)


product1 = Product("Laptop", 1000)
product2 = Product("Mouse", 50)

print(f"\n{product1.name}: ${product1.get_total_price():.2f}")
print(f"{product2.name}: ${product2.get_total_price():.2f}")

product1.tax_rate = 0.2
print(f"\nAfter changing tax for laptop:")
print(f"{product1.name}: ${product1.get_total_price():.2f}")
print(f"{product2.name}: ${product2.get_total_price():.2f}")

Product.tax_rate = 0.15
print(f"\nAfter changing class tax rate:")
print(f"{product1.name}: ${product1.get_total_price():.2f}")
print(f"{product2.name}: ${product2.get_total_price():.2f}")


# Example 4
class GameCharacter:
    total_characters = 0
    default_health = 100

    def __init__(self, name, character_type):
        self.name = name
        self.character_type = character_type
        self.health = GameCharacter.default_health
        GameCharacter.total_characters += 1

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} took {damage} damage. Health: {self.health}")

    @classmethod
    def get_total_characters(cls):
        return cls.total_characters


warrior = GameCharacter("Conan", "Warrior")
mage = GameCharacter("Gandalf", "Mage")

print(f"\nTotal characters: {GameCharacter.get_total_characters()}")
warrior.take_damage(30)
mage.take_damage(50)