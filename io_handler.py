"""
IO_HANDLER.PY
-------------
Handles user input collection only.
"""
import utils
from constants import MINUTES_PER_DAY

def get_tasks_from_user():
    """Loops to ask user for tasks until they type 'done'."""
    print("\n--- TASK INPUT ---\nType 'done' when finished.")
    tasks = []
    
    while True:
        name = input("\nTask name (or 'done'): ").strip()
        if name.lower() == 'done': break

        dur = utils.parse_duration(input("Duration (e.g., 90m): "))
        earliest = utils.parse_time(input("Earliest Start (HH:MM): ")) or 0
        latest = utils.parse_time(input("Latest End (HH:MM): ")) or MINUTES_PER_DAY
        days_str = input("Specific days (Mon,Wed) or enter: ")
        prio = input("Priority (S, A, B, C): ").upper()
        
        try:
            freq = int(input("Times per week: "))
        except ValueError:
            freq = 1

        pref_days = [d.strip().title() for d in days_str.split(',')] if days_str else []

        tasks.append({
            'name': name, 'duration': dur,
            'earliest_min': earliest, 'latest_min': latest,
            'frequency': freq, 'min_days_between': 0,
            'preferred_days': pref_days,
            'priority': prio if prio in 'SABCD' else 'C'
        })
    return tasks