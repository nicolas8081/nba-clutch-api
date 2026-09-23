import sqlite3
import pandas as pd

# this connects to the database file
connection = sqlite3.connect("data/nba.sqlite")
# tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", connection)
# sample = pd.read_sql_query("SELECT * FROM game LIMIT 5;", connection)
# pbp = pd.read_sql_query("SELECT * FROM play_by_play LIMIT 10;", connection)
# print("COLUMNS:", list(pbp.columns))
# print(pbp.head(10).to_string())
# pbp = pd.read_sql_query("SELECT * FROM play_by_play LIMIT 10;", connection)
# print("COLUMNS:", list(pbp.columns))
# print(pbp.head(10).to_string())
q = """
SELECT game_date_est,
       team_abbreviation_home, pts_qtr4_home, pts_home,
       team_abbreviation_away, pts_qtr4_away, pts_away
FROM line_score
ORDER BY game_date_est DESC
LIMIT 10;
"""
sample = pd.read_sql_query(q, connection)
print(sample.to_string())

# Check the date range so we know "last 10 years" is available
rng = pd.read_sql_query(
    "SELECT MIN(game_date_est) AS earliest, MAX(game_date_est) AS latest FROM line_score;", connection
)
print(rng)

# Check for missing Q4 values (our cleaning target)
nulls = pd.read_sql_query(
    "SELECT COUNT(*) AS missing_q4 FROM line_score WHERE pts_qtr4_home IS NULL OR pts_qtr4_home = '';", connection
)
print(nulls)
connection.close()