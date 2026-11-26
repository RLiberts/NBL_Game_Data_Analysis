import json
from pathlib import Path
from datetime import datetime
from db import get_connection
from parse_game import duration_to_seconds, parse_players, parse_events

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

UPSERT_GAME = """
MERGE dbo.Games AS t
USING (SELECT ? AS GameId, ? AS SeasonId, ? AS VenueId, ? AS StartTimeLocal, ? AS StartTimeUtc, ? AS Status, ? AS GameType, ? AS Attendance)
AS s ON t.GameId = s.GameId
WHEN MATCHED THEN UPDATE SET SeasonId = s.SeasonId, VenueId = s.VenueId, StartTimeLocal = s.StartTimeLocal, StartTimeUtc = s.StartTimeUtc, Status = s.Status, GameType = s.GameType, Attendance = s.Attendance
WHEN NOT MATCHED THEN INSERT (GameId, SeasonId, VenueId, StartTimeLocal, StartTimeUtc, Status, GameType, Attendance) VALUES (s.GameId, s.SeasonId, s.VenueId, s.StartTimeLocal, s.StartTimeUtc, s.Status, s.GameType, s.Attendance);
"""

DELETE_GAME_DATA = [
"DELETE FROM dbo.GameEvents WHERE GameId = ?",
"DELETE FROM dbo.PlayerGameStats WHERE GameId = ?",
"DELETE FROM dbo.GamePeriodScores WHERE GameId = ?",
"DELETE FROM dbo.GameTeams WHERE GameId = ?",
]

INSERT_GAME_TEAM = """
INSERT INTO dbo.GameTeams (GameId, TeamId, IsHome, Score, TeamReboundsOffensive, TeamReboundsDefensive, TeamTurnovers, TeamFouls, BiggestLead, TimeInLeadSeconds, LeadChanges, PointsInPaint, PointsFromBench)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

INSERT_PERIOD_SCORE = """
INSERT INTO dbo.GamePeriodScores (GameId, TeamId, PeriodId, Points)
VALUES (?, ?, ?, ?);
"""

INSERT_PLAYER_STATS = """
INSERT INTO dbo.PlayerGameStats (GameId, PlayerId, TeamId, Bib, Position, IsStarter, Participated, Seconds, Points, TwoPtMade, TwoPtAttempted, ThreePtMade,
ThreePtAttempted, FreeThrowsMade, FreeThrowsAttempted, ReboundsOffensive,ReboundsDefensive, Assists, Turnovers, Steals, Blocks, Fouls, PlusMinus, Efficiency)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

INSERT_EVENT = """
INSERT INTO dbo.GameEvents (EventId, GameId, EventSeq, PeriodId, ClockSeconds, TeamId, PlayerId, EventType, EventSubType, Success, X, Y)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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

def load_game_row(cursor, box: dict) -> None:

    fixture = box["data"]["fixture"]

    cursor.execute(
        UPSERT_GAME, fixture["fixtureId"], fixture["seasonId"], fixture["venueId"],
        datetime.fromisoformat(fixture["startTimeLocal"]), datetime.fromisoformat(fixture["startTimeUTC"]),
        fixture["status"],fixture["fixtureType"], fixture ["attendance"]
    )
    print(f"Datums {fixture['startTimeLocal'][:10]}, {fixture['status']}, skatītāji {fixture['attendance']}")


def delete_game_data(cursor, game_id: str) -> None:
    for sql in DELETE_GAME_DATA:
        cursor.execute(sql, game_id)


def load_game_teams(cursor, box: dict) -> None:
    game_id = box["data"]["fixture"]["fixtureId"]
    base = box["data"]["statistics"]["data"]["base"]

    for team in box["data"]["fixture"]["competitors"]:
        side = "home" if team["isHome"] else "away"
        extra = base[side]["extra"]
        totals = base[side]["totalEntityStats"]
        score = int(team["score"]) if team["score"] is not None else None

        cursor.execute(
            INSERT_GAME_TEAM,
            game_id, team["entityId"], team["isHome"], score, extra["reboundsOffensive"], extra["reboundsDefensive"], extra["turnovers"], extra["foulsTotal"],
            totals["biggestLead"], duration_to_seconds(totals["timeInLead"]),totals["leadChanges"], totals["pointsInThePaint"], totals["pointsFromBench"]
        )


def load_period_scores(cursor, box: dict) -> None:
    game_id = box["data"]["fixture"]["fixtureId"]
    rows = []
    for period in box["data"]["periodData"]:
        for team_id, points in period["teamScore"].items():
            rows.append((game_id, team_id, period["periodId"], points))
    cursor.executemany(INSERT_PERIOD_SCORE, rows)
    print(f"Periodi: {len(rows)} rindas")

def load_player_stats(cursor, fixture_id: str) -> None:
    rows = []
    for p in parse_players(fixture_id):
        rows.append((
            p["fixture_id"], p["person_id"], p["team_id"], p["bib"], p["position"], p["starter"], p["participated"], p["seconds"],
            p["points"], p["pointsTwoMade"], p["pointsTwoAttempted"],
            p["pointsThreeMade"], p["pointsThreeAttempted"],
            p["freeThrowsMade"], p["freeThrowsAttempted"],
            p["reboundsOffensive"], p["reboundsDefensive"],
            p["assists"], p["turnovers"], p["steals"], p["blocks"],
            p["foulsTotal"], p["plusMinus"], p["efficiency"]
        ))
    cursor.executemany(INSERT_PLAYER_STATS, rows)
    print(f"Spēlētāju statistika: {len(rows)} rindas")

def load_events(cursor, fixture_id: str) -> None:
    rows = []
    for e in parse_events(fixture_id):
        rows.append((
            e["event_id"], e["fixture_id"], e["event_seq"], e["period"],
            e["clock_seconds"], e["team_id"], e["person_id"],
            e["event_type"], e["event_sub_type"], e["success"], e["x"], e["y"]
        ))
    cursor.executemany(INSERT_EVENT, rows)
    print(f"Notikumi: {len(rows)} rindas")


def load_game(fixture_id: str) -> None:
    box = load_json(fixture_id, "box")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.fast_executemany = True
        try:
            load_reference_data(cursor, box)
            load_game_row(cursor, box)
            delete_game_data(cursor, fixture_id)
            load_game_teams(cursor, box)
            load_period_scores(cursor, box)
            load_player_stats(cursor, fixture_id)
            load_events(cursor, fixture_id)
            conn.commit()
            print(f"Spēle ielādēta: {fixture_id}")
        except Exception:
            conn.rollback()
            print(f"Kļūda, spēle {fixture_id} netika saglabāta")
            raise


if __name__ == "__main__":
    load_game("5bea1909-b03d-11f1-94f9-8fdd370562ae")