= Criterion A: Problem specification

== Problem scenario

Each week I lose valuable time by manually planning my schedule for the upcoming week. I need to fit coursework (EE drafts, IA write-ups, homework) around deadlines and fixed events like lessons and my tennis trainings, by taking a list of tasks, estimating how long each takes, and assigning deadlines and priorities. This creates a system where everything is affected by _everything_ else. Therefore when a new task comes up during the week, or a deadline is changed, I need to manually replan the entire schedule. This turns out to be not only time consuming, but also unreliable: I overload some days, leave others empty, and notice too late when a task no longer fits before its deadline.

I want a tool where I can enter my tasks (with a *duration*, *deadline*, and *priority*) together with my fixed events and the number of hours I'm willing to spend working per day. This will then be used to automatically produce a conflict-free schedule that places tasks before their deadlines, properly prioritizes them, and reports anything that cannot fit.

== Why a computational solution fits

Fitting a set amount of tasks into limited free time around fixed events is a combinatorics problem. The number of possible arrangements grows rapidly, and each combination has to be validated against several constraints at once (overlaps, deadlines, daily capacity). This is exactly the repetitive rule based search a computer performs quickly and consistently. Meanwhile I, the human, do it slowly and make mistakes. Therefore the problem requires an algorithm.

I will build a terminal program in *Python 3, standard library only*: `datetime` for deadline arithmetic on 15-minute blocks, and `json` for human-readable persistence. Python is fully suitable for this task without adding unnecessary complexities or dependencies, and it's a language I've been learning and can explain line by line. I also looked at existing tools: *Google Calendar* stores events but cannot place tasks, since it has no concept of a deadline-constrained job to fit into free time, and *Todoist* ranks a to-do list by date and priority but never checks whether the work actually _fits_ before its deadline, so infeasibility goes undetected. Both record decisions; neither _computes_ a placement.

== Success criteria

The solution is successful if:

+ Tasks (name, duration, deadline, priority) and events (name, start, end) can be added, edited, and deleted via a menu.
+ No scheduled task overlaps another task or a fixed event.
+ Every scheduled task finishes on or before its deadline.
+ A task that cannot fit before its deadline is *reported* with its name, shortfall, and deadline, never just ignored.
+ Daily scheduled work never exceeds the user-set limit.
+ A task longer than one free gap is split across days, with each part showing progress (e.g. `1h30 of 4h00`).
+ Adding, editing, or deleting a task, event, or config value regenerates a valid schedule.
+ All data (tasks, events, config, schedule) persists in a JSON file between sessions.
+ Invalid input (past deadline, non-positive duration, malformed time) is rejected with a specific message.
+ Both strategies, *earliest-deadline-first* and *priority-first*, run on the same input and print each one's missed-deadline count and priority-weighted on-time work, so the choice between them is measured.
