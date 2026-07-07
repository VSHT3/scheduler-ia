"""
data.py — builds and validates the records our scheduler works with.

A "record" is one bundle of related information stored as a dict.
For now this file knows how to build ONE kind of record: a task.
"""

from datetime import datetime


def make_task(name, duration, deadline, priority, tags=None):
    # tags=None (default value, simplifies further validation)

    # VALIDATIONS
    if name.strip() == "":  # name can't be empty
        raise ValueError("Task name cannot be empty.")

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
    # deadline must be text in ISO format (2027-07-11T17:00)
    if not isinstance(deadline, str):  # checks for deadline being text
        raise ValueError('Deadline must be text, e.g. "2027-07-11T17:00".')
    try:
        deadline_dt = datetime.fromisoformat(deadline)
        # tries converting the str to ISO date
    except ValueError:
        raise ValueError("Deadline must be a valid date-time, e.g. 2027-07-11T17:00.")

    # 15 minute rule + no seconds
    if deadline_dt.minute % 15 != 0 or deadline_dt.second != 0:
        raise ValueError("Deadline minutes must be :00, :15, :30 or :45.")

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
        "deadline": deadline_dt,  # datetime object not text (the `deadline` var)
        "priority": priority,  # int
        "tags": clean_tags,  # list of labels e.g. ["cs", "ia"]
    }
    return task
