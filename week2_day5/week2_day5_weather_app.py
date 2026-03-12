import requests
from config import API_KEY
import json
import os

def load_history():
    if os.path.exists("weather_history.json"):
        try:
            with open("weather_history.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading weather history.")
            return []
    return []

def save_history(history):
    with open("weather_history.json", "w") as file:
        json.dump(history, file, indent=4)

def get_weather(city):
    
    url = f"https://api.openweathermap.org/data/2.5/weather?id=524901&q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url,timeout=10)

        if response.status_code == 200:
            data = response.json()

            city_name = data["name"]
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]

            print("\nWeather Report:")
            print(f"City: {city_name}")
            print(f"Temperature: {temp}°C")
            print(f"Condition: {weather}")

            return{
                "city": city_name,
                "temperature": temp,
                "condition": weather
            }
        
        else:
            print("Error fetching weather data. Please check the city name and try again.")
            return None
        
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching weather data:", e)

        return None

def main():
   
   history = load_history()

   while True:

        city = input("\nEnter city name (or type 'quit'): ")

        if city.lower() == "quit":
            print("Goodbye!")
            break
        result = get_weather(city)

        if result:
            history.append(result)
            save_history(history)
            print("Weather data saved to history.")
    
if __name__ == "__main__":
    main()