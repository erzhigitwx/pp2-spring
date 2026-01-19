# Integer casting
x = int(1)
y = int(2.8)   # => 2
z = int("3")   # => 3
print(x)
print(y)
print(z)

# Float casting
x = float(1)     # => 1.0
y = float(2.8)   # => 2.8
z = float("3")   # => 3.0
w = float("4.2") # => 4.2
print(x)
print(y)
print(z)
print(w)

# String casting
x = str("s1")  # => 's1'
y = str(2)     # => '2'
z = str(3.0)   # => '3.0'
print(x)
print(y)
print(z)

# Casting and type checking
x = int(5.7)
print(x)
print(type(x))

# Practical casting example
age = "25"
age_int = int(age)
next_year = age_int + 1
print("Current age:", age_int)
print("Next afe:", next_year)