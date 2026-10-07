import duckdb
import pandas as pd
ON_TIME_MINUTES = 5
con = duckdb.connect('mbta.duckdb')

pred_df = con.sql('SELECT * FROM predictions').df()
sched_df = con.sql('SELECT * FROM schedules').df()



pred_sorted = pred_df.sort_values('pulled_at')
latest_df = pred_sorted.drop_duplicates(subset=['trip_id', 'stop_id'],keep='last').copy()

latest_df['duration'] = latest_df['arrival_time'] - latest_df['pulled_at']
latest_df['gap_minutes'] = latest_df['duration'].dt.total_seconds() / 60


newest = pred_df['pulled_at'].max()
close_enough = (latest_df['gap_minutes'] <= 10)
not_newest = (latest_df['pulled_at'] != newest)
scoreable_df = latest_df[close_enough & not_newest]


res = pd.merge(scoreable_df,sched_df,on=['trip_id', 'stop_id'], suffixes=('_predicted','_scheduled'),indicator=True,how='left')
matched = res[res['_merge'] == 'both'].copy()
matched['lateness'] = matched['arrival_time_predicted'] - matched['arrival_time_scheduled']
matched['lateness_minutes'] = matched['lateness'].dt.total_seconds() / 60
matched['on_time'] = matched['lateness_minutes'] <= ON_TIME_MINUTES

print(f"On time: {matched['on_time'].mean():.1%} (n = {len(matched)})")

