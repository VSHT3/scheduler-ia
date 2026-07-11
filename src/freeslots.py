# freeslots.py
from datetime import datetime


def make_freeslots(day, events, config):
    # init data
    block_start = datetime.combine(day, config["workstart"])
    block_end = datetime.combine(day, config["workend"])
    cursor=block_start
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
