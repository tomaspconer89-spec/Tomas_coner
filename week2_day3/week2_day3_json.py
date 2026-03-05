class User:
    def __init__(self,name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def to_dict(self):
        return {
            "name": self.name,
            "city": self.city,
            "age": self.age
        }

