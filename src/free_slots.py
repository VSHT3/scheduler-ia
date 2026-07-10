#yap here
from datetime import date, time, datetime


day = date(2027,7,12)
events = [
    {
        "name": "School",
        "start": datetime(2027, 7, 12, 8, 0),
        "end": datetime(2027, 7, 12, 15, 0),
        "repeat": "none",
    },
    {
        "name": "School",
        "start": datetime(2027, 7, 12, 8, 0),
        "end": datetime(2027, 7, 12, 17, 0),
        "repeat": "none",
    },
    {
        "name": "School",
        "start": datetime(2027, 7, 12, 8, 0),
        "end": datetime(2027, 7, 12, 22, 0),
        "repeat": "none",
    },
    {
        "name": "Hockey practice",
        "start": datetime(2027, 7, 12, 16, 0),
        "end": datetime(2027, 7, 12, 18, 0),
        "repeat": "none",
    },
    {
        "name": "Dinner",
        "start": datetime(2027, 7, 12, 16, 0),
        "end": datetime(2027, 7, 12, 19, 15),
        "repeat": "none",
    },
]


config = {
    "workstart": time(7, 0),
    "workend": time(22, 0),
    "daily_cap": 300,
    "horizon": 7,
    "heuristic": "edf",
}
block_start = datetime.combine(day, config["workstart"])
block_end = datetime.combine(day, config["workend"])

cursor=block_start
sorted_events = sorted(events, key=lambda event: event["start"]) # sorted list orders things based on asc start

free_slots=[]
previous_end=datetime(1,1,1,1,1)
for sorted_event in sorted_events:
    if  block_start < sorted_event["start"] and sorted_event["end"] < block_end: # big blocker, ignore for now
        break
    elif cursor < sorted_event["start"]:
        if sorted_event["start"] < previous_end and sorted_event["end"] > previous_end:
            free_slots.pop()
            free_slots.append((cursor,sorted_event["start"]))
        else:
            previous_start=sorted_event["start"]
            previous_end=sorted_event["end"]
            free_slots.append((cursor,sorted_event["start"]))
            cursor=sorted_event["end"]
    else:
        pass




#def free_slots(day, config, events):
 #   block_start = datetime.combine(day, config["workstart"])
  #  block_end = datetime.combine(day, config["workend"])
