import requests

API_KEY = '56f20452-9276-4c35-91c8-a1bacb4cb32f'

CITY = "Moradabad"
STATE = "Uttar Pradesh"
COUNTRY = "INDIA"

# API url
url = f"https://api.airvisual.com/v2/city?city={CITY}&state={STATE}&country={COUNTRY}&key={API_KEY}"

# make a request to the API
response = requests.get(url)
data = response.json()

# Extract AQI
try:
    aqi = data['data']['current']['pollution']['aqius']
    print(f"The Air Quality Index (AQI) for {CITY}, {STATE}, {COUNTRY} is: {aqi}")
except :
    print("Failed to retrieve AQI. Check your API key or location details.")
