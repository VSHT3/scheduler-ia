## Criterion A, Problem specification

### Problem scenario

Each week I lose valuable time by manually planning my schedule for the upcoming week. I need to plan around deadlines and fixed events (like lessons and my tennis trainings) by taking a list of tasks, estimating how long each takes and assigning deadlines and priorities. This creates a system where everything is affected by *everything* else. Therefore when a new task comes up during the week, or a deadline is changed, I need to manually replan the entire schedule. This turns out to be not only time consuming, but also unreliable since I sometimes miss deadlines or overload some days.

I want a tool where I can enter my tasks together with my fixed events and number of hours I'm willing to spend working. This will then be used to automatically produce a conflict-free schedule that properly prioritizes my tasks. 

### Why a computational solution fits

Fitting a set amount of tasks into a limited free time around fixed events is a combinatorics problem. The number of possible arrangements grows rapidly, and each combination has to be validated against several constraints (overlaps, deadlines, working hours, daily capacity, etc). This is exactly the repetitive rule based search a computer performs quickly and consistently. Meanwhile I, the human, do it slowly and make mistakes. 
Therefore the problem requires an algorithm. I chose **Python** as a language of execution, because it's fully suitable for this task without adding unnecessary complexities or dependencies.  It's also a language I've been learning, and I have a basic understanding of.

### Success criteria

The solution is successful if:
1. No scheduled task overlaps another task or a fixed event.
2. Every task ends on or before its deadline (if it's infeasible in a schedule, it is **reported**, never just ignored).
3. Daily scheduled work never exceeds a user-set limit.
4. A task longer than one day is split. 
5. Adding, editing, or deleting a task or event regenerates a valid schedule.
6. Schedule, as well as it's events, tasks, and config, persist between sessions. 