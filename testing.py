# import requests

# url = "https://httpbin.org/get"
# params = {"email": "ishaantanwar1511@gmail.com"}

# response = requests.get(url, params=params)
# print(response.json())  # This should return the expected output



import re
import pandas as pd
from datetime import datetime

# Sample scraped descriptions (replace with actual BeautifulSoup extraction)
descriptions = [
    "A clear sky and a moderate breezeSunny and a moderate breezeLight cloud and a moderate breeze",
    "Light rain and a gentle breezeSunny intervals and a moderate breezeLight cloud and a gentle breeze"
]

# ✅ Step 1: Split descriptions properly using regex
# ✅ Step 1: Extract text from BeautifulSoup Tag before processing
weather_descriptions = []
for desc in descriptions:
    text = desc.get_text(strip=True)  # Extract text safely
    split_descriptions = re.findall(r'[a-zA-Z][^A-Z]*', text)  # Properly split descriptions
    weather_descriptions.extend([s.strip() for s in split_descriptions if s.strip()])  # Clean and store


# ✅ Step 2: Generate Date List (starting from today)
datelist = pd.date_range(datetime.today(), periods=len(weather_descriptions)).tolist()
datelist = [date.strftime('%Y-%m-%d') for date in datelist]  # Correct format

# ✅ Step 3: Create JSON Dictionary
forecast_data = {datelist[i]: weather_descriptions[i] for i in range(len(datelist))}

# ✅ Output JSON
print(forecast_data)
