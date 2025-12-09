import scheduler
from datetime import date, timedelta

tasks = [{
    'name': 'Study',
    'duration': 60,
    'earliest_min': 540,
    'latest_min': 1020,
    'frequency': 1,
    'min_days_between': 0,
    'preferred_days': ['Monday', 'Tuesday'],
    'priority': 'A'
}]

daily, dates = scheduler.assign_tasks_to_days(tasks)
print("Week starts:", dates[0].strftime("%A, %b %d"))
for i, day_tasks in enumerate(daily):
    day_name = dates[i].strftime("%A")
    print(f"{day_name}: {len(day_tasks)} tasks")
