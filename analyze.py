import duckdb
import pandas as pd

con = duckdb.connect('mbta.duckdb')

pred_df = con.sql('SELECT * FROM predictions').df()
sched_df = con.sql('SELECT * FROM schedules').df()
