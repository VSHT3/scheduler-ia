# yap here
import json
import data # imports data.py for data.def references


# SAVING
def save(path, tasks, events, config):
    tasks_to_save = []
    for task in tasks:
        clean = {
            "name": task["name"],
            "duration": task["duration"],
            "deadline": task["deadline"].isoformat(),
            "priority": task["priority"],
            "tags": task["tags"]
        }
        tasks_to_save.append(clean)

    events_to_save = []
    for event in events:
        clean = {
            "name": event["name"],
            "start": event["start"].isoformat(),
            "end": event["end"].isoformat(),
            "repeat": event["repeat"],
        }
        events_to_save.append(clean)

    config_to_save = {
        "workstart": config["workstart"].isoformat(),
        "workend": config["workend"].isoformat(),
        "daily_cap": config["daily_cap"],
        "horizon": config["horizon"],
        "heuristic": config["heuristic"],
    }

    all_data = {
        "tasks": tasks_to_save,
        "events": events_to_save,
        "config": config_to_save,
    }

    with open(path, "w") as file:
        json.dump(all_data, file, indent=2)

# LOAD
def load(path):
    try:
        with open(path, "r") as file: # tries opening our data file if we have it
            all_data = json.load(file) #loads a dictionary of 2 lists and 1 dictionary into all_data
    except FileNotFoundError:
        return [],[],data.make_config("08:00","22:00",300,7,"edf") # if we don't have a data file, it creates one with empty events and tasks, and a default config

    section = "file" # default for error message if somethign is wrong even before try: loads
    index= 0 # default for error message if somethign is wrong even before try: loads
    try:
        section = "task" # capture section for error handling
        # re-validate tasks by checking each list entry (a dict) with make_task and return them into a single list
        tasks = []
        for index, task in enumerate(all_data["tasks"]): #enumare to properly count index
            clean_task = data.make_task(task["name"],task["duration"],task["deadline"],task["priority"],task["tags"])
            tasks.append(clean_task)

        section = "events" # capture section for error handling
        # re-validate events by checking each list entry (a dict) with make_event and return them into a single list
        events = []
        for index, event in enumerate(all_data["events"]): #enumare to properly count index
            clean_event = data.make_event(event["name"],event["start"],event["end"],event["repeat"])
            events.append(clean_event)

        section = "config" # capture section for error handling
        index = 0 # index 0 since config by itself doesn't have an index
        #re-validate config (just a dict) with make_config
        dirty_config = all_data["config"]
        config = data.make_config(dirty_config["workstart"],dirty_config["workend"],dirty_config["daily_cap"],dirty_config["horizon"],dirty_config["heuristic"])

        #return everything
        return tasks,events,config
    except (ValueError, KeyError) as error:
        raise ValueError(f"Data file '{path}' is corrupted at {section} #{index} \n{error}")
