# Example 1
def add(a, b):
    return a + b

result = add(5, 3)
print(f"5 + 3 = {result}")
print(f"10 + 20 = {add(10, 20)}")

# Example 2
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

print(f"Score 85 -> Grade: {get_grade(85)}")
print(f"Score 92 -> Grade: {get_grade(92)}")

# Example 3
def get_min_max(numbers):
    return min(numbers), max(numbers)

nums = [5, 2, 9, 1, 7]
minimum, maximum = get_min_max(nums)
print(f"Numbers: {nums}")
print(f"Min: {minimum}, Max: {maximum}")

# Example 4
def calculate_circle(radius):
    pi = 3.14159
    area = pi * radius ** 2
    circumference = 2 * pi * radius
    return area, circumference

area, circ = calculate_circle(5)
print(f"Circle with radius 5:")
print(f"Area: {area:.2f}")
print(f"Circumference: {circ:.2f}")

# Example 5
def get_person_info(name, age, city):
    return {
        "name": name,
        "age": age,
        "city": city,
        "adult": age >= 18
    }

person = get_person_info("Alice", 25, "London")
print(f"Person info: {person}")
print(f"Name: {person['name']}")
print(f"Is adult: {person['adult']}")

# Example 6
def is_even(number):
    if number % 2 == 0:
        return True
    return False

print(f"4 is even: {is_even(4)}")
print(f"7 is even: {is_even(7)}")