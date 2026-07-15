# schedule.py takes tasks + free slots and places each task into a slot before its deadline (EDF for now)


from datetime import timedelta


def schedule_tasks(tasks,config,freeslots,current_time):
    scheduled_tasks = []
    past_deadline = False # flag for tasks whose deadline has already passed
    past_deadline_tasks = [] # keep the already-late ones separate so we don't silently drop them
    sorted_tasks = []
    temp_tasks = sorted(tasks, key=lambda task: task["deadline"]) # earliest deadline first
    for task in temp_tasks:
        if task["deadline"] <= current_time: # deadline is already in the past, can't schedule it
            past_deadline = True
            past_deadline_tasks.append(task)
        else:
            sorted_tasks.append(task) # still schedulable, goes into the pool

    # earliest-deadline-first (EDF)
    for i in range(len(freeslots)): # walk each day in the horizon
        current_day = freeslots[i]
        for j in range(len(current_day)): # walk each free slot in that day
            start,end = current_day[j]
            for task in list(sorted_tasks): # copy the list so removing from it mid-loop doesn't skip tasks
                slot_duration = end - start
                if slot_duration >= timedelta(minutes=15): ## check if free slot is at least 15 mins (the minimum time for a task)
                    task_duration = timedelta(minutes=task["duration"]) # set task_duration as minutes
                    if start + task_duration <= task["deadline"]: # only place it if it actually finishes before the deadline
                        if task_duration <= slot_duration: ## If a task fits into the slot
                            scheduled_task = dict(task) # New independent dictionary
                            scheduled_task["start"] = start
                            scheduled_task["end"] = start + task_duration
                            scheduled_tasks.append(scheduled_task)
                            sorted_tasks.remove(task) # placed, so pull it out of the list
                            start = scheduled_task["end"] # move cursor forward so the next task starts after this one
    print(f"Missed tasks: {sorted_tasks}") # anything left in the list never fit before its deadline
    return scheduled_tasks


                    # if task_duration + timedelta(minutes=10) ## BREAK TIME LOGIC

#Deadline is the latest time when a task can be done.
