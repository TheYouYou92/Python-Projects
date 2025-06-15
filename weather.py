from security import safe_requests


API_KEY = "###################"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

city = input("Enter a city name: ")

request_url = f"{BASE_URL}?q={city}&appid={API_KEY}"

response = safe_requests.get(request_url)
if response.status_code == 200:
    data = response.json()
    weather = data['weather'][0]['description']
    temprerature = round(data['main']['temp'] - 273.15, 2)
    print("Weather: ", weather)
    print("Temperature: ", temprerature)
else:
    print("En Error occured")
