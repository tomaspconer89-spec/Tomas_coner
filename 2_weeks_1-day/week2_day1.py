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
    
user1 = User("Tomas", "London", 25)
user2 = User("Alice", "New York", 15)

print(user1.introduce())
print(user2.introduce())