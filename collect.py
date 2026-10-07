import duckdb 
import pandas as pd
from fetch import get_predictions,get_schedules

def table_exists(con, table_name, schema="main"):
    query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ? AND table_name = ?"
    result = con.execute(query, [schema,table_name]).fetchone()
    return result[0] > 0

con = duckdb.connect('mbta.duckdb')

pred_rows = get_predictions("Red")
pred_df = pd.DataFrame(pred_rows)
pred_df['arrival_time'] = pd.to_datetime(pred_df['arrival_time'])
pred_df['departure_time'] = pd.to_datetime(pred_df['departure_time'])
pred_df['pulled_at'] = pd.to_datetime(pred_df['pulled_at'])

if table_exists(con, 'predictions'):
    con.execute('INSERT INTO predictions SELECT * FROM pred_df')
else: con.execute('CREATE TABLE predictions AS SELECT * FROM pred_df')

sched_rows = get_schedules("Red")
sched_df = pd.DataFrame(sched_rows)
sched_df['arrival_time'] = pd.to_datetime(sched_df['arrival_time'])
sched_df['departure_time'] = pd.to_datetime(sched_df['departure_time'])

if table_exists(con, 'schedules'):
    con.execute('INSERT INTO schedules SELECT * FROM sched_df WHERE schedule_id NOT IN (SELECT schedule_id FROM schedules)')
else: con.execute('CREATE TABLE schedules AS SELECT * FROM sched_df')

print(f"Saved: Predictions = {con.sql('SELECT COUNT(*) FROM predictions').fetchone()[0]}, Schedules = {con.sql('SELECT COUNT(*) FROM schedules').fetchone()[0]}")
