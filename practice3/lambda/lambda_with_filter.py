# Example 1
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print(f"All numbers: {numbers}")
print(f"Even numbers: {even_numbers}")

# Example 2
words = ["apple", "hi", "banana", "cat", "elephant", "dog"]
long_words = list(filter(lambda word: len(word) > 3, words))

print(f"\nAll words: {words}")
print(f"Words longer than 3 letters: {long_words}")

# Example 3
numbers = [-5, 3, -1, 7, -8, 0, 12]
positive = list(filter(lambda x: x > 0, numbers))

print(f"\nAll numbers: {numbers}")
print(f"Positive numbers: {positive}")

# Example 4
ages = [15, 22, 18, 34, 12, 45, 17, 28]
adults = list(filter(lambda age: 18 <= age < 65, ages))

print(f"\nAll ages: {ages}")
print(f"Adult ages (18-64): {adults}")

# Example 5
data = ["hello", "", "world", "", "python", " "]
non_empty = list(filter(lambda s: s.strip(), data))

print(f"\nAll data: {data}")
print(f"Non-empty strings: {non_empty}")

# Example 6
students = [
    {"name": "Alice", "score": 85, "age": 20},
    {"name": "Bob", "score": 92, "age": 19},
    {"name": "Charlie", "score": 65, "age": 21},
    {"name": "David", "score": 78, "age": 18}
]

top_students = list(filter(lambda s: s["score"] >= 80, students))

print("\nTop students (score >= 80):")
for student in top_students:
    print(f"  {student['name']}: {student['score']}")

# Example 7
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

numbers = range(1, 21)
primes = list(filter(lambda x: is_prime(x), numbers))

print(f"\nNumbers 1-20: {list(numbers)}")
print(f"Prime numbers: {primes}")

# Example 8
products = [
    {"name": "Laptop", "price": 999, "in_stock": True},
    {"name": "Mouse", "price": 25, "in_stock": False},
    {"name": "Keyboard", "price": 75, "in_stock": True},
    {"name": "Monitor", "price": 299, "in_stock": True}
]

affordable = list(filter(lambda p: p["price"] < 500 and p["in_stock"], products))

print("\nAffordable products in stock:")
for product in affordable:
    print(f"  {product['name']}: ${product['price']}")