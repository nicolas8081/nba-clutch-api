import sqlite3
import pandas as pd

DB_PATH = "data/nba.sqlite"

def load_line_scores(db_path: str = DB_PATH) -> pd.DataFrame:
    # the columns will be loaded from the line score table
    query = """
        SELECT game_date_est,
               team_abbreviation_home, pts_qtr4_home, pts_home,
               team_abbreviation_away, pts_qtr4_away, pts_away
        FROM line_score
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    num_cols = ["pts_qtr4_home", "pts_home", "pts_qtr4_away", "pts_away"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["game_date_est"] = pd.to_datetime(df["game_date_est"], errors="coerce")
    df = df.dropna(subset=num_cols + ["game_date_est"])
    latest = df["game_date_est"].max()
    cutoff = latest - pd.DateOffset(years=10)
    df = df[df["game_date_est"] >= cutoff]

    df = df.reset_index(drop=True)
    conn.close()
    return df
if __name__ == "__main__":
    df = load_line_scores()
    print(df.shape)
    print(df.head())