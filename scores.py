import sqlite3


def dict_factory(cur, row):  # Возвращает данные в виде словаря
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


def add_score(username, score, cell, speed, time):
    if score > 0:
        array = [username, score, cell, speed, time]
        cursor.execute("INSERT INTO Scores (Username, Score, Cell, Speed, Time) VALUES (?, ?, ?, ?, ?)", array)
        conn.commit()


def get_scores(cell, speed):
    cursor.execute("SELECT * FROM Scores WHERE Cell = ? AND Speed = ? ORDER BY Score DESC limit 10", (cell, speed))
    return cursor.fetchall()


conn = sqlite3.connect("scores.sqlite")
conn.row_factory = dict_factory
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Scores(
Username TEXT NOT NULL,
Score TEXT NOT NULL,
Cell INT NOT NULL,
Speed INT NOT NULL,
Time TEXT NOT NULL
)
""")
conn.commit()


