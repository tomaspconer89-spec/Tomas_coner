from week2_day1 import User

def main():
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

if __name__ == "__main__":
    main()