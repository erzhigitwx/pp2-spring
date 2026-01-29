# Example 1: Basic elif
a = 33
b = 33
if b > a:
    print("b is greater than a")
elif a == b:
    print("a and b are equal")

# Example 2: Multiple elif with else
score = 75
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")

# Example 3: Age categories
age = 35
if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
elif age < 60:
    print("Adult")
else:
    print("Senior")

# Example 4: Time of day
hour = 14
if hour < 12:
    print("Good morning")
elif hour < 18:
    print("Good afternoon")
else:
    print("Good evening")

# Example 5: Temperature ranges
temp = 22
if temp < 0:
    print("Freezing")
elif temp < 10:
    print("Cold")
elif temp < 20:
    print("Cool")
elif temp < 30:
    print("Warm")
else:
    print("Hot")