#yap here
from datetime import date, time, datetime


day = date(2027,7,12)
events = []


config = {
    "workstart": time(7, 0),
    "workend": time(23, 0),
    "daily_cap": 300,
    "horizon": 7,
    "heuristic": "edf",
}



block_start = datetime.combine(day, config["workstart"])
block_end = datetime.combine(day, config["workend"])

cursor=block_start
sorted_events = sorted(events, key=lambda event: event["start"]) # sorted list orders things based on asc start
number_of_events = len(sorted_events)

free_slots=[]
if events == []:
    free_slots.append((block_start,block_end))
else:
    for index, sorted_event in enumerate(sorted_events):
        if sorted_event["start"] <= block_start and block_end <= sorted_event["end"]: # big blocker, ignore for now
            print("huge event, full day")
            break # return empty free_slots
        elif block_end <= sorted_event["end"]: # checks if an event ends after blockend
            free_slots.append((cursor,sorted_event["start"]))
            print("day is finished")
            break
        elif index == (number_of_events-1):
            if cursor < sorted_event["start"]:
                free_slots.append((cursor,sorted_event["start"]))
                free_slots.append((sorted_event["end"],block_end))
        elif sorted_event["start"] <= cursor: # checks if event start <=cursor
            if sorted_event["end"] > cursor: # the "stairs" problem
                cursor=sorted_event["end"]
            else: # the "smaller event within a bigger event" problem
                print("smaller event within a bigger event is ignored, just to be sure")
                pass
                #ignore
        else:
            free_slots.append((cursor,sorted_event["start"]))
            cursor=sorted_event["end"]

print(free_slots)



#def free_slots(day, config, events):
 #   block_start = datetime.combine(day, config["workstart"])
  #  block_end = datetime.combine(day, config["workend"])
