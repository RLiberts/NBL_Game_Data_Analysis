import requests
import json
import time
from pathlib import Path  
from state import SEASON_ID, encode_state

BASE_URL = "https://embed-api.eui.connect.sportradar.com/v1/embed/120"
RAW = Path("raw") 
PAUSE = 2.5

def fetch_json(state: dict, file_path: Path)-> dict:
    if file_path.exists():
        print(f"Fails jau eksistē: {file_path}")
        return json.loads(file_path.read_text(encoding="utf-8"))
    url = f"{BASE_URL}/fixture_detail?state={encode_state(state)}"
    time.sleep(PAUSE)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    RAW.mkdir(exist_ok=True)
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saglabāts: {file_path}")
    return data

if __name__ == "__main__":
    fixture_id = "5bea1909-b03d-11f1-94f9-8fdd370562ae"
    box = fetch_json({"s": SEASON_ID, "l": "lv-LV", "f": fixture_id}, RAW / f"{fixture_id}_box.json")
    print(f"Statuss: {box['data']['fixture']['status']}")
    pbp = fetch_json({"s": SEASON_ID, "l": "lv-LV", "z": "pbp", "f": fixture_id}, RAW / f"{fixture_id}_pbp.json")
    print(f"Ceturtdaļas: {len(pbp['data']['periodData'])}")