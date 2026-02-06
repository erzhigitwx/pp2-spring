# Example 1
numbers = [-5, 3, -1, 7, -8, 2]
sorted_by_abs = sorted(numbers, key=lambda x: abs(x))

print(f"Original: {numbers}")
print(f"Sorted by absolute value: {sorted_by_abs}")

# Example 2
words = ["python", "hi", "programming", "code", "a"]
sorted_by_length = sorted(words, key=lambda word: len(word))

print(f"\nOriginal words: {words}")
print(f"Sorted by length: {sorted_by_length}")

# Example 3
numbers = [5, 2, 8, 1, 9]
descending = sorted(numbers, key=lambda x: x, reverse=True)

print(f"\nOriginal: {numbers}")
print(f"Descending: {descending}")

# Example 4
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("David", 95)]
sorted_by_score = sorted(students, key=lambda student: student[1], reverse=True)

print("\nStudents sorted by score (highest first):")
for name, score in sorted_by_score:
    print(f"  {name}: {score}")

# Example 5
products = [
    {"name": "Laptop", "price": 999},
    {"name": "Mouse", "price": 25},
    {"name": "Keyboard", "price": 75},
    {"name": "Monitor", "price": 299}
]

sorted_by_price = sorted(products, key=lambda p: p["price"])

print("\nProducts sorted by price:")
for product in sorted_by_price:
    print(f"  {product['name']}: ${product['price']}")

# Example 6
employees = [
    {"name": "Alice", "dept": "IT", "salary": 80000},
    {"name": "Bob", "dept": "HR", "salary": 60000},
    {"name": "Charlie", "dept": "IT", "salary": 90000},
    {"name": "David", "dept": "HR", "salary": 65000}
]

sorted_employees = sorted(employees, key=lambda e: (e["dept"], -e["salary"]))

print("\nEmployees sorted by dept, then salary (desc):")
for emp in sorted_employees:
    print(f"  {emp['name']} - {emp['dept']}: ${emp['salary']}")

# Example 7
words = ["apple", "pie", "zoo", "alpha", "beta"]
sorted_by_last = sorted(words, key=lambda w: w[-1])

print(f"\nWords: {words}")
print(f"Sorted by last letter: {sorted_by_last}")
