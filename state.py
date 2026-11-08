import zlib
import base64
import json

Season_ID = "a60432f8-9a2b-11f1-b5e1-d9d221ebbf47" #Ramirent NBL 2026/27

def encode_state(state: dict) -> str:
    text = json.dumps(state) #dict uz json
    json_bytes = text.encode('utf-8') #json uz baitiem
    compressed = zlib.compress(json_bytes) #saspiesti baiti
    encoded = base64.urlsafe_b64encode(compressed) #saspiesti baiti uz base64 baitiem
    return encoded.decode("ascii").rstrip("=") #uz tekstu un noņem = beigās

if __name__ == "__main__":
    result = encode_state({"s": Season_ID, "l": "lv-LV", "z": "RESULTS"})
    print(result)
    print(result == "eJyrVipWslJQSjQzMDE2SrPQtUw0StI1NEwz1E0yTTXUTbFMMTIyTE1KSjMxV9JRUMoBKc4p0_UJA_GqQLwg1-BQn5BgpVoAzboTCQ")