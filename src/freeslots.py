# freeslots.py turns fixed events + working hours into the empty gaps where tasks can go
from datetime import time, datetime, timedelta


def split_events(events): # an event spanning multiple days gets chopped into one piece per day
    split_events=[]
    for event in events:
        current = event["start"]
        if current.date() != event["end"].date(): # event crosses midnight into another day
            split_event = dict(event)
            split_event["start"] = current
            split_event["end"] = datetime.combine(current.date(), time(23,59,59))
            split_events.append(split_event)
            while current.date() != event["end"].date():
                current += timedelta(days=1) # increment event[start]
                if current.date() == event["end"].date(): # this is the last day of the split
                    split_event = dict(event)
                    split_event["start"] = datetime.combine(current.date(), time(0,0))
                    split_events.append(split_event)
                else:
                    split_event = dict(event)
                    split_event["start"] = datetime.combine(current.date(), time(0,0))
                    split_event["end"] = datetime.combine(current.date(), time(23,59,59))
                    split_events.append(split_event)
        else:
            split_events.append(event)
    return split_events

def make_day_freeslots(today, events, config): # builds the free gaps for a single day

    # init data
    block_start = datetime.combine(today, config["workstart"]) # start of my working hours today
    block_end = datetime.combine(today, config["workend"]) # end of my working hours today
    cursor=block_start # cursor walks along the day, marking where the last event left off
    sorted_events = sorted(events, key=lambda event: event["start"]) # sorted list orders things based on asc start
    ignore_last_event = False
    free_slots=[]
    if events == []:
        free_slots.append((block_start,block_end)) # no events, so the whole working day is free
    else:
        for sorted_event in sorted_events:
            if sorted_event["start"].date() == today:
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

def make_horizon_freeslots(today,horizon,events,config): # runs the day builder across every day in the horizon
    split_events_list = split_events(events)
    freeslots=[]
    for i in range(horizon):
        horizon_day = today + timedelta(days=i)
        day_freeslots = make_day_freeslots(horizon_day,split_events_list,config)
        freeslots.append(day_freeslots)
    return freeslots
