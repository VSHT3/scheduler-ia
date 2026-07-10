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
    with open(path, "r") as file:
        all_data = json.load(file)
    return all_data

# TODO: DOUBLE CHECK BY REUSING make defs from @data.py
