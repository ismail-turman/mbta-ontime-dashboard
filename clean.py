import pandas as pd
from fetch import get_predictions,get_schedules,get_routes
import duckdb

# arrival_time is null for a trips first stop (train starts from there, doesn't arrive)
# departure_time is null for a trips last stop (train ends there, doesn't depart)
# pulled_at is when this snapshot was taken (set to UTC), same value for every row in one run
# arrival_time, departure_time, and pulled_at are all timezone-aware datetimes 

pred_rows = get_predictions("Red")
pred_df = pd.DataFrame(pred_rows)
pred_df['arrival_time'] = pd.to_datetime(pred_df['arrival_time'])
pred_df['departure_time'] = pd.to_datetime(pred_df['departure_time'])
pred_df['pulled_at'] = pd.to_datetime(pred_df['pulled_at'])

# duckdb vv
con = duckdb.connect('mbta.duckdb')

def table_exists(con, table_name, schema="main"):
    query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ? AND table_name = ?"
    result = con.execute(query, [schema,table_name]).fetchone()
    return result[0] > 0

if table_exists(con, 'predictions'):
    con.execute('INSERT INTO predictions SELECT * FROM pred_df')
else: con.execute('CREATE TABLE predictions AS SELECT * FROM pred_df')
#print(con.sql("SELECT COUNT(*) FROM predictions"))


# calculating minutes until arrival
pred_df['time_until_arrival'] = pred_df['arrival_time'] - pred_df['pulled_at']
pred_df['minutes_until_arrival'] = pred_df['time_until_arrival'].dt.total_seconds() / 60

# merging prediction df and schedule df
sched_rows = get_schedules("Red")
sched_df = pd.DataFrame(sched_rows)
pred_df['arrival_time'] = pd.to_datetime(pred_df['arrival_time'])
pred_df['departure_time'] = pd.to_datetime(pred_df['departure_time'])
pred_df['pulled_at'] = pd.to_datetime(pred_df['pulled_at'])

sched_df['arrival_time'] = pd.to_datetime(sched_df['arrival_time'])
sched_df['departure_time'] = pd.to_datetime(sched_df['departure_time'])

res = pd.merge(pred_df,sched_df,on=['stop_id', 'trip_id'], suffixes=('_predicted','_scheduled'))

res['lateness'] = res['arrival_time_predicted'] - res['arrival_time_scheduled']
res['lateness_minutes'] = res['lateness'].dt.total_seconds() / 60
res['on_time'] = res['lateness_minutes'] <= 15

print(f"On time: {res['on_time'].mean():.1%} (n = {len(res)})")