import requests 

url = "https://api.github.com"

response = requests.get(url)

print("status code:", response.status_code)

data = response.json()

print("API message:", data["current_user_url"])