import requests
from state import encode_state, Season_ID

base_URL = "https://embed-api.eui.connect.sportradar.com/v1/embed/120"
fixture_ID= "5bea1909-b03d-11f1-94f9-8fdd370562ae"

#Izveid protokola URL
state = encode_state({"s": Season_ID, "l": "lv-LV", "f": fixture_ID})
url = f"{base_URL}/fixture_detail?state={state}"
print(url)

#Nosūta piieprasījumu
response = requests.get(url, timeout=30)
print("Statuss:", response.status_code)

#Pārvērš atbildi uz vārdnīcu
data = response.json()
print("Atslēgas:", list(data["data"].keys()))
print("Spēles statuss", data["data"]["fixture"]["status"])