# Example 1: Basic boolean values
print(10 > 9)
print(10 == 9)
print(10 < 9)

# Example 2: Boolean in if statement
a = 200
b = 33
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Example 3: Evaluate values with bool()
print(bool("Hello"))
print(bool(15))

# Example 4: False values
print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

# Example 5: Functions returning boolean
def myFunction():
    return True

print(myFunction())