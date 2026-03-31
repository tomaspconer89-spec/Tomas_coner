from weather_service import get_weather
from history_manager import load_history, save_history

def main():
    history = load_history()

    while True:
        
        print("\n 1. Get Weather")
        print("2. View History")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            city = input("Enter city name: ")
            result = get_weather(city)

            if result:
                print("\nWeather Report:")
                print(result)

                history.append(result)
                save_history(history)
                print("Weather data saved to history.")
        
        elif choice == "2":
            if history:
                print("\nWeather History:")
                for entry in history:
                    print(f"{entry['city']}: {entry['temperature']}°C, {entry['description']}")
            else:
                print("No history found.")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()