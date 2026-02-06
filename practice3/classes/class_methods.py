# Example 1
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count

    def reset(self):
        self.count = 0


counter = Counter()
counter.increment()
counter.increment()
print(f"Count: {counter.get_count()}")
counter.reset()
print(f"After reset: {counter.get_count()}")


# Example 2
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def circumference(self):
        return 2 * 3.14159 * self.radius

    def scale(self, factor):
        self.radius *= factor
        print(f"New radius: {self.radius}")


circle = Circle(5)
print(f"\nCircle radius: {circle.radius}")
print(f"Area: {circle.area():.2f}")
print(f"Circumference: {circle.circumference():.2f}")
circle.scale(2)

# Example 3
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, name, price):
        self.items.append({"name": name, "price": price})
        self.total += price
        print(f"Added {name} (${price})")

    def remove_item(self, name):
        for item in self.items:
            if item["name"] == name:
                self.items.remove(item)
                self.total -= item["price"]
                print(f"Removed {name}")
                return
        print(f"{name} not found")

    def show_cart(self):
        print(f"\n=== Shopping Cart ===")
        for item in self.items:
            print(f"  {item['name']}: ${item['price']}")
        print(f"Total: ${self.total}")


cart = ShoppingCart()
cart.add_item("Laptop", 999)
cart.add_item("Mouse", 25)
cart.show_cart()
cart.remove_item("Mouse")
cart.show_cart()


# Example 4
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def to_fahrenheit(self):
        return (self.celsius * 9 / 5) + 32

    def to_kelvin(self):
        return self.celsius + 273.15

    def set_celsius(self, value):
        self.celsius = value

    def display_all(self):
        print(f"\n{self.celsius}°C")
        print(f"{self.to_fahrenheit()}°F")
        print(f"{self.to_kelvin()}K")


temp = Temperature(25)
temp.display_all()

# Example 5
class Game:
    def __init__(self, player_name):
        self.player = player_name
        self.score = 0
        self.level = 1

    def play_round(self, points_earned):
        self.score += points_earned
        print(f"{self.player} earned {points_earned} points")
        self.check_level_up()

    def check_level_up(self):
        required_score = self.level * 100
        if self.score >= required_score:
            self.level += 1
            print(f"🎉 Level up! Now at level {self.level}")

    def show_stats(self):
        print(f"\n=== {self.player}'s Stats ===")
        print(f"Level: {self.level}")
        print(f"Score: {self.score}")


game = Game("Alice")
game.play_round(50)
game.play_round(60)
game.show_stats()