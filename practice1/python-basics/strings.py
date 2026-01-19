# 1) Creating strings
x = "Hello"
y = 'Hello'
print(x)
print(y)

# 2) Multiline strings
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

# 3) Strings with indexing
a = "Hello, World!"
print(a[0])     # First character
print(a[1])     # Second character
print(a[-1])    # Last character

# 4) String slicing
b = "Hello, World!"
print(b[2:5])   # Characters from position 2 to 5 (not included)
print(b[:5])
print(b[2:])
print(b[-5:-2]) # Negative indexing

# 5) String methods and operations
a = "Hello, World!"
print(len(a))              # Length
print(a.upper())           # Convert to uppercase
print(a.lower())           # Convert to lowercase
print(a.replace("H", "J")) # Replace characters
print(a.split(","))        # Split string into list