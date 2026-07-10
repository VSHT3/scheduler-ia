# data.py builds and validates records for my scheduler
from datetime import datetime, time


# NAME CHECKER
def _parse_name(text, label):
    if not isinstance(text, str):
        raise ValueError(f"{label} must be text, e.g. 'Task 1', not '{text}'.")
    text = text.strip()
    if text == "":
        raise ValueError(f"{label} cannot be empty.")
    return text


# ISO PARSER
# must be text in ISO format (2027-07-11T17:00) OR only time (08:00)
def _parse_iso_datetime(text, label, parser):
    if not isinstance(text, str):  # checks for input being text
        raise ValueError(
            f"{label} must be text, not '{text}', e.g. '2027-07-11T17:00' for datetime or '08:00' for time."
        )
    try:
        value = parser(text)
        # tries converting the str to ISO date
    except ValueError:
        raise ValueError(
            f"{label} must be a valid time or date-time, not '{text}', e.g. 08:00 or 2027-07-11T17:00."
        )
    # 15 minute rule + no seconds
    if value.minute % 15 != 0 or value.second != 0:
        raise ValueError(
            f"{label} minutes can't be '{value}' must be :00, :15, :30 or :45 and seconds are not permitted."
        )
    return value


# IS IN LIST CHECKER
def _is_in_list(value, allowed, label):
    if isinstance(value, str):
        value = value.strip().lower()  # sanitize if string
    if value not in allowed:  # priority is only 1/2/3
        raise ValueError(f"{label} ({value}) must be in {allowed}.")
    return value


# DURATION CHECKER
# duration must be a whole number of minutes, positive, divisible by 15
def _minute_duration_parser(duration, label):
    if not isinstance(duration, int):
        raise ValueError(f"{label} can't be '{duration}', and must be a whole number of minutes.")
    if duration <= 0:
        raise ValueError(f"{label} can't be '{duration}', and must be greater than zero.")
    if duration % 15 != 0:
        raise ValueError(f"{label} can't be '{duration}', and must be a multiple of 15 minutes.")
    return duration


# TASK MAKER
def make_task(name, duration, deadline, priority, tags=None):
    # tags=None (default value, simplifies further validation)

    # VALIDATIONS
    # NAME
    name = _parse_name(name, "Task name")

    # DURATION
    duration = _minute_duration_parser(duration, "Task duration")
    # PRIORITY
    priority = _is_in_list(priority, (1, 2, 3), "Task priority")

    # DEADLINE
    deadline = _parse_iso_datetime(deadline, "Task deadline", datetime.fromisoformat)
    # TAGS
    if tags is None:
        tags = []  # -> start from an empty list

    clean_tags = []
    for tag in tags:
        # convert to str then remove spaces, lowercase, drop a leading '#', trim again.
        t = str(tag).strip().lower()
        t = t.lstrip("#").strip()
        if (
            t and t not in clean_tags
        ):  # skip blanks (if t="" it returns 0) and duplicates
            clean_tags.append(t)

    # BUILD the task dictionary
    task = {
        "name": name,  # string
        "duration": duration,  # int
        "deadline": deadline,  # datetime object not text (the `deadline` var)
        "priority": priority,  # int
        "tags": clean_tags,  # list of labels e.g. ["cs", "ia"]
    }
    return task


# EVENT MAKER
def make_event(
    name, start, end, repeat="none"
):  # default repeat to 'none', easier for validation than None
    # VALIDATIONS

    # NAME
    name = _parse_name(name, "Event name")
    # START
    start = _parse_iso_datetime(start, "Event start", datetime.fromisoformat)
    # END
    end = _parse_iso_datetime(end, "Event end", datetime.fromisoformat)
    # REPEAT
    repeat = _is_in_list(repeat, ("daily", "weekly", "none"), "Event repeat")

    # VALIDATE temporality
    if end <= start:
        raise ValueError("Event must start before it ends.")

    event = {
        "name": name,
        "start": start,
        "end": end,
        "repeat": repeat,
    }
    return event


def make_config(workstart, workend, daily_cap, horizon, heuristic="edf"):
    workstart = _parse_iso_datetime(workstart, "Config workstart", time.fromisoformat)
    workend = _parse_iso_datetime(workend, "Config workend", time.fromisoformat)

    # VALIDATE temporality
    if workend <= workstart:
        raise ValueError("Work must start before it ends.")

    daily_cap = _minute_duration_parser(daily_cap, "Config daily cap")

    # HORIZON
    if not isinstance(horizon, int):
        raise ValueError(f"Horizon must be a whole number of days, not '{horizon}'.")
    if horizon <= 0:
        raise ValueError(f"Horizon must be greater than zero, not '{horizon}'.")

    # HEURISTIC
    heuristic = _is_in_list(heuristic, ("edf", "priority"), "Config heuristic")

    config = {
        "workstart": workstart,
        "workend": workend,
        "daily_cap": daily_cap,
        "horizon": horizon,
        "heuristic": heuristic,
    }
    return config
