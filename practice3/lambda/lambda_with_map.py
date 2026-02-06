# Example 1
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))

print(f"Original: {numbers}")
print(f"Squared: {squared}")

# Example 2
names = ["alice", "bob", "charlie"]
capitalized = list(map(lambda name: name.capitalize(), names))

print(f"\nOriginal names: {names}")
print(f"Capitalized: {capitalized}")

# Example 3
numbers1 = [1, 2, 3, 4]
numbers2 = [10, 20, 30, 40]
sums = list(map(lambda x, y: x + y, numbers1, numbers2))

print(f"\nList 1: {numbers1}")
print(f"List 2: {numbers2}")
print(f"Sums: {sums}")

# Example 4
celsius = [0, 10, 20, 30, 40]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))

print(f"\nCelsius: {celsius}")
print(f"Fahrenheit: {fahrenheit}")

# Example 5
prices = [19.99, 29.50, 99.99, 5.00]
formatted = list(map(lambda p: f"${p:.2f}", prices))

print(f"\nPrices: {prices}")
print(f"Formatted: {formatted}")

# Example 6
students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 92},
    {"name": "Charlie", "score": 78}
]

def add_grade(student):
    score = student["score"]
    if score >= 90:
        student["grade"] = "A"
    elif score >= 80:
        student["grade"] = "B"
    else:
        student["grade"] = "C"
    return student

students_with_grades = list(map(add_grade, students))
for student in students_with_grades:
    print(f"{student['name']}: {student['score']} ({student['grade']})")

# Example 7
data = ["  hello  ", "  world  ", "  python  "]
cleaned = list(map(lambda s: s.strip().upper(), data))

print(f"\nOriginal data: {data}")
print(f"Cleaned: {cleaned}")