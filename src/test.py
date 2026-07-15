from datetime import datetime, timedelta

start = datetime(2026, 7, 16, 9, 0)
end = datetime(2026, 7, 16, 17, 0)

duration = end - start


task_duration = timedelta(minutes=3000)

if duration > task_duration:
    print(f"Yes, duration is greater than task ({duration} > {task_duration})")

print(start, end)
print(duration)
