import pandas as pd
from fetch import get_predictions
import duckdb

# arrival_time is null for a trips first stop (train starts from there, doesn't arrive)
# departure_time is null for a trips last stop (train ends there, doesn't depart)
# pulled_at is when this snapshot was taken (set to UTC), same value for every row in one run
# arrival_time, departure_time, and pulled_at are all timezone-aware datetimes 

rows = get_predictions("Red")
df = pd.DataFrame(rows)
df['arrival_time'] = pd.to_datetime(df['arrival_time'])
df['departure_time'] = pd.to_datetime(df['departure_time'])
df['pulled_at'] = pd.to_datetime(df['pulled_at'])


con = duckdb.connect('mbta.duckdb')

def table_exists(con, table_name, schema="main"):
    query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ? AND table_name = ?"
    result = con.execute(query, [schema,table_name]).fetchone()
    return result[0] > 0

if table_exists(con, 'predictions'):
    con.execute('INSERT INTO predictions SELECT * FROM df')
else: con.execute('CREATE TABLE predictions AS SELECT * FROM df')

print(con.sql("SELECT COUNT(*) FROM predictions"))