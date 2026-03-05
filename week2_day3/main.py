from week2_day3_json import User
import os
import json

file_path = "users.json"

def main():
#step 1: check if file exists
    if os.path.exists(file_path):
        try:
            with open(file_path,"r") as file:
                users_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users_list =  []
    else:
        users_list =  []
    
#step 2: create a new user and add to the list
    name = input("Enter your name: ")    
    city = input("Enter your city: ")
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Invalid age. Please enter a valid integer.")
        return
    
    user = User(name, city, age)
    user_data = user.to_dict()
    users_list.append(user_data)

#step 3: save the updated list back to the file
    with open("users.json", "w") as file:
        json.dump(users_list, file, indent=4)
        print("User data saved to users.json successfully.")
    print(f"Current users in file: {len(users_list)}")

if __name__ == "__main__":
    main()