import requests
from config import API_KEY, BASE_URL

def get_weather(city):

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url,timeout=10)

        if response.status_code == 200:
            data = response.json()

            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }
        else:
            print("City not found.")
            return None

    except requests.exceptions.RequestException:
        print("Network error occurred.")
        return None