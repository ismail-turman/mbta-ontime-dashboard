# mbta-ontime-dashboard 

WIP: pipeline fetches predictions + schedules from the MBTA V3 API,
matches them, and computes on-time % (currently Red Line only).

On-time definition: arrival within 5 minutes of scheduled time.
The arrival I score is the MBTA's last prediction, not a measured arrival.