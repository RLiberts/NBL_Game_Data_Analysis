import json
import csv
from pathlib import Path

RAW = Path("raw")
DATA = Path("data")

STAT_FIELDS = [
    "minutes", "points", "pointsTwoMade", "pointsTwoAttempted", 
    "pointsThreeMade", "pointsThreeAttempted", "freeThrowsMade", "freeThrowsAttempted",
    "reboundsOffensive", "reboundsDefensive", "rebounds",
    "assists", "turnovers", "steals", "blocks", "foulsTotal", "plusMinus", "efficiency"
]
def duration_to_seconds(value: str | None) -> int | None:
    if not value:
        return None
    value = value.removeprefix("PT")
    minutes = 0
    seconds = 0
    if "M" in value:
        m, value = value.split("M")
        minutes = int(m)
    if "S" in value:
        seconds = int(value.removesuffix("S"))
    return minutes * 60 + seconds

def parse_players(fixture_id: str)-> list[dict]:
    box = json.loads((RAW / f"{fixture_id}_box.json").read_text(encoding="utf-8"))
    base = box["data"]["statistics"]["data"]["base"]

    rows = []
    for side in ("home", "away"):
        for player in base[side]["persons"][0]["rows"]:
            row = {"fixture_id": fixture_id,
                "side": side,
                "team_id": player["entityId"],
                "person_id": player["personId"],
                "name": player["personName"],
                "bib": player["bib"],
                "starter": player["starter"],
                "participated": player["participated"]
            }
            for field in STAT_FIELDS:
                row[field] = player["statistics"].get(field)
            row["seconds"] = duration_to_seconds(row.pop("minutes"))
            rows.append(row)
    return rows

def parse_events(fixture_id: str) -> list[dict]:
    pbp = json.loads((RAW / f"{fixture_id}_pbp.json").read_text(encoding="utf-8"))

    rows = []
    for period in pbp["data"]["periodData"]:
        for event in period["events"]:
            rows.append({
                "fixture_id": fixture_id, "event_id": event["eventId"],
                "period": event["periodId"], "clock_seconds": duration_to_seconds(event["clock"]),
                "event_type": event["eventType"], "event_sub_type": event["eventSubType"], "success": event["success"],
                "person_id": event["personId"], "team_id": event["entityId"],
                "x": event["x"], "y": event["y"]
            })
    return rows

def write_csv(rows: list[dict], file_path: Path) -> None:
    DATA.mkdir(exist_ok=True)
    with file_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saglabāts: {file_path} ({len(rows)} rindas)")

if __name__ == "__main__":
    fixture_id = "5bea1909-b03d-11f1-94f9-8fdd370562ae"
    players = parse_players(fixture_id)
    write_csv(players, DATA / f"{fixture_id}_players.csv")
    events = parse_events(fixture_id)
    write_csv(events, DATA / f"{fixture_id}_events.csv")


    for field in ("points", "seconds"):
        totals = {}
        for p in players:
            totals[p["side"]] = totals.get(p["side"], 0) + (p[field] or 0)
        print(f"{field} pa komandām: {totals}")

    points_map = {"2pt": 2, "3pt": 3, "freeThrow": 1}
    event_points = {}
    for e in events:
        if e["success"] and e["event_type"] in points_map:
            team = e["team_id"]
            event_points[team] = event_points.get(team, 0) + points_map[e["event_type"]]
    print("Punkti no spēles gaitas:", event_points)