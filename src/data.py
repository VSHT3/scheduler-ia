# data.py builds and validates records for my scheduler
from datetime import datetime


# TASK MAKER
def make_task(name, duration, deadline, priority, tags=None):
    # tags=None (default value, simplifies further validation)

    # VALIDATIONS
    # NAME
    name = _parse_name(name, "Task name")

    # DURATION
    # duration must be a whole number of minutes, positive, divisible by 15
    if not isinstance(duration, int):
        raise ValueError("Duration must be a whole number of minutes.")
    if duration <= 0:
        raise ValueError("Duration must be greater than zero.")
    if duration % 15 != 0:
        raise ValueError("Duration must be a multiple of 15 minutes.")

    # PRIORITY
    if priority not in (1, 2, 3):  # priority is only 1/2/3
        raise ValueError("Priority must be 1 (LOW), 2 (MEDIUM) or 3 (HIGH).")

    # DEADLINE
    deadline = _parse_iso_datetime(deadline, "Task deadline")
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
        ):  # skip blanks (if t=[""] it returns 0) and duplicates
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


# NAME PARSER
def _parse_name(text, label):
    if not isinstance(text, str):
        raise ValueError(f"{label} must be text, e.g. 'Task 1'.")
    text = text.strip()
    if text == "":
        raise ValueError(f"{label} cannot be empty.")
    return text


# ISO PARSER
# must be text in ISO format (2027-07-11T17:00)
def _parse_iso_datetime(text, label):
    if not isinstance(text, str):  # checks for input being text
        raise ValueError(f"{label} must be text, e.g. '2027-07-11T17:00'.")
    try:
        dt = datetime.fromisoformat(text)
        # tries converting the str to ISO date
    except ValueError:
        raise ValueError(f"{label} must be a valid date-time, e.g. 2027-07-11T17:00.")
    # 15 minute rule + no seconds
    if dt.minute % 15 != 0 or dt.second != 0:
        raise ValueError(
            f"{label} minutes must be :00, :15, :30 or :45. Seconds are not permitted."
        )
    return dt


def make_event(
    name, start, end, repeat="none"
):  # default repeat to 'none', easier for validation than None
    # VALIDATIONS

    # NAME
    name = _parse_name(name, "Event name")

    # START
    start = _parse_iso_datetime(start, "Event start")

    # END
    end = _parse_iso_datetime(end, "Event end")

    # REPEAT
    repeat = str(repeat).strip().lower()
    if repeat not in ("daily", "weekly", "none"):
        raise ValueError(f"{repeat} is not 'daily', 'weekly', or 'none' text.")

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
