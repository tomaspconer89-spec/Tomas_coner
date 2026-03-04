class User:
    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def greet(self):
        return f"Hello, My name is {self.name} and I live in {self.city}"
    
    def is_adult(self):
        return self.age >= 18
    
    def introduce(self):
        intro = self.greet()
        if self.is_adult():
            return intro
        else:
            return intro + " I am a minor."
    
name = input("Enter your name: ")
city = input("Enter your city: ")
try:
    age = int(input("Enter your age:  "))
except ValueError:
    print("Invalid input for age. Please enter a number.")
    age = 0
    
user = User(name, city, age)

with open("users.txt", "a") as file:
    file.write(user.introduce() + "\n")
    print("User saved to users.txt successfully.")