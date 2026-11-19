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

def load_json(fixture_id: str, kind: str) -> dict:
    return json.loads((RAW / f"{fixture_id}_{kind}.json").read_text(encoding="utf-8")) #kind ir 'pbp' vai 'box'

if __name__ == "__main__":
    fixture_id = "5bea1909-b03d-11f1-94f9-8fdd370562ae"
    box = load_json(fixture_id, "box")
    season = box["data"]["banner"]["season"]

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPSERT_SEASON, season["id"], season["name"])
        conn.commit()
        print("Sezona ielādēta:", season["name"])
