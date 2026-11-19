import json
from pathlib import Path
from db import get_connection

RAW = Path("raw")

UPSERT_SEASON = """
MERGE dbo.Seasons AS t
USING (SELECT ? AS SeasonId, ? AS Name) AS s
ON t.SeasonId = s.SeasonId
WHEN MATCHED THEN UPDATE SET Name = s.Name
WHEN NOT MATCHED THEN INSERT (SeasonId, Name) VALUES (s.SeasonId, s.Name);
"""

UPSERT_TEAM = """
MERGE dbo.Teams AS t
USING (SELECT ? AS TeamId, ? AS Name, ? AS Code) AS s
ON t.TeamId = s.TeamId
WHEN MATCHED THEN UPDATE SET Name = s.Name, Code = s.Code
WHEN NOT MATCHED THEN INSERT (TeamId, Name, Code) VALUES (s.TeamId, s.Name, s.Code);
"""

UPSERT_VENUE = """
MERGE dbo.Venues AS t
USING (SELECT ? AS VenueId, ? AS Name) AS s
ON t.VenueId = s.VenueId
WHEN MATCHED THEN UPDATE SET Name = s.Name
WHEN NOT MATCHED THEN INSERT (VenueId, Name) VALUES (s.VenueId, s.Name);
"""

UPSERT_PLAYER = """
MERGE dbo.Players AS t
USING (SELECT ? AS PlayerId, ? AS Name) AS s
ON t.PlayerId = s.PlayerId
WHEN MATCHED THEN UPDATE SET Name = s.Name
WHEN NOT MATCHED THEN INSERT (PlayerId, Name) VALUES (s.PlayerId, s.Name);
"""

def load_json(fixture_id: str, kind: str) -> dict:
    return json.loads((RAW / f"{fixture_id}_{kind}.json").read_text(encoding="utf-8")) #kind ir 'pbp' vai 'box'

def load_reference_data(cursor, box: dict) -> None:

    fixture = box["data"]["fixture"]

    season = box["data"]["banner"]["season"]
    cursor.execute(UPSERT_SEASON, season["id"], season["name"])

    for team in fixture["competitors"]:
        cursor.execute(UPSERT_TEAM, team["entityId"], team["name"], team["code"])

    if fixture["venueId"]:
        cursor.execute(UPSERT_VENUE, fixture["venueId"], fixture["venue"])

    base = box["data"]["statistics"]["data"]["base"]
    players = []
    for side in ("home", "away"):
        for p in base[side]["persons"][0]["rows"]:
            players.append((p["personId"], p["personName"]))
    cursor.executemany(UPSERT_PLAYER, players)
    print(f"{len(fixture['competitors'])} komandas, {len(players)} spēlētāji")


if __name__ == "__main__":
    fixture_id = "5bea1909-b03d-11f1-94f9-8fdd370562ae"
    box = load_json(fixture_id, "box")
    season = box["data"]["banner"]["season"]

    with get_connection() as conn:
        cursor = conn.cursor()
        load_reference_data(cursor, box)
        conn.commit()
