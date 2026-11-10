import pyodbc

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=RLIBERTS;"
    "DATABASE=NBL;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


def get_connection() -> pyodbc.Connection:
    """Atver savienojumu ar NBL datubāzi."""
    return pyodbc.connect(CONNECTION_STRING)


if __name__ == "__main__":
    with get_connection() as conn:
        row = conn.execute("SELECT @@VERSION").fetchone()
        print(row[0])