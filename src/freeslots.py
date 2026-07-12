# freeslots.py
from datetime import time, datetime, timedelta


def split_events(events):
    split_events=[]
    for event in events:
        if event["start"].date() != event["end"].date():
            split_event={
                "name": event["name"],
                "start": event["start"],
                "end": datetime.combine(event["start"].date(), time(23,59,59)),
                "repeat": event["repeat"],
            }
            split_events.append(split_event)
            while event["start"].date() != event["end"].date():
                event["start"] = event["start"] + timedelta(days=1) # increment event[start]
                if event["start"].date() == event["end"].date(): # this is the last day of the split
                    split_event={
                        "name": event["name"],
                        "start": datetime.combine(event["start"].date(), time(0,0)),
                        "end": event["end"],
                        "repeat": event["repeat"],
                    }
                    split_events.append(split_event)
                else:
                    split_event={
                        "name": event["name"],
                        "start": datetime.combine(event["start"].date(), time(0,0)),
                        "end": datetime.combine(event["start"].date(), time(23,59,59)),
                        "repeat": event["repeat"],
                    }
                    split_events.append(split_event)
        else:
            split_events.append(event)
    return split_events

def make_day_freeslots(today, events, config):

    # init data
    block_start = datetime.combine(today, config["workstart"])
    block_end = datetime.combine(today, config["workend"])
    cursor=block_start
    events = split_events(events)
    sorted_events = sorted(events, key=lambda event: event["start"]) # sorted list orders things based on asc start
    ignore_last_event = False
    free_slots=[]
    if events == []:
        free_slots.append((block_start,block_end))
    else:
        for sorted_event in sorted_events:
            if sorted_event["start"] <= block_start and block_end <= sorted_event["end"]: # big blocker, ignore for now
                ignore_last_event=True
                break # return empty free_slots
            elif block_end <= sorted_event["end"]: # checks if an event ends after blockend
                free_slots.append((cursor,sorted_event["start"]))
                ignore_last_event=True
                break
            elif sorted_event["start"] <= cursor: # checks if event start <=cursor
                if sorted_event["end"] > cursor: # the "stairs" problem
                    cursor=sorted_event["end"]
            else:
                free_slots.append((cursor,sorted_event["start"]))
                cursor=sorted_event["end"]
            #end loop
        if cursor < block_end and not ignore_last_event:
            free_slots.append((cursor,block_end))
    return free_slots


def make_horizon_freeslots(today,horizon,events,config):
