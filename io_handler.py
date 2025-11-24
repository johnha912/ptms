"""
IO_HANDLER.PY
-------------
Handles Input/Output.
This file contains the code that talks to the human user.
It handles `input()` and `print()`.
"""

import csv
import utils
from constants import MINUTES_PER_DAY

def get_tasks_from_user():
    """
    Loops to ask user for tasks until they type 'done'.
    Returns a list of dictionaries.
    """
    print("\n--- TASK INPUT ---")
    print("Type 'done' when finished.")
    
    tasks = []
    
    while True:
        name = input("\nTask name (or 'done'): ").strip()
        if name.lower() == 'done':
            break

        # Get raw strings
        dur_str = input("Duration (e.g., 90m, 1.5h): ")
        early_str = input("Earliest Start (HH:MM or enter): ")
        late_str = input("Latest End (HH:MM or enter): ")
        freq_str = input("Times per week (default 1): ")
        days_str = input("Specific days (Mon,Wed) or enter: ")
        prio_str = input("Priority (S, A, B, C): ").upper()

        # Clean/Convert data using utils
        duration = utils.parse_duration(dur_str)
        earliest = utils.parse_time(early_str) or 0
        latest = utils.parse_time(late_str) or MINUTES_PER_DAY
        
        try:
            frequency = int(freq_str)
        except ValueError:
            frequency = 1

        preferred_days = []
        if days_str:
            # List comprehension to clean up comma-separated string
            preferred_days = [d.strip().capitalize() for d in days_str.split(',')]

        # Save to dictionary
        tasks.append({
            'name': name,
            'duration': duration,
            'earliest_min': earliest,
            'latest_min': latest,
            'frequency': frequency,
            'min_days_between': 0, # Simplified for beginner version
            'preferred_days': preferred_days,
            'priority': prio_str if prio_str in 'SABCD' else 'C'
        })

    return tasks

def visualize_schedule(viz_data, week_dates):
    """
    Prints a visual ASCII bar chart of the week.
    RENAMED from print_visualization to match test_scenarios.py
    """
    print("\n" + "=" * 60)
    print("SCHEDULE VISUALIZATION")
    print("=" * 60)

    for i, items in enumerate(viz_data):
        if not items: continue

        day_name = week_dates[i].strftime("%A, %b %d")
        print(f"\n{day_name}")
        print("-" * 60)

        # Sort tasks by time so they print in order
        # We use .get() to handle errors safely
        sorted_items = sorted(items, key=lambda x: x.get('start_min', 9999))

        for item in sorted_items:
            if 'start_min' in item:
                # Calculate bar length: 1 char per 15 mins
                bar_len = item['duration'] // 15
                bar = "█" * min(bar_len, 40) # Max width 40 chars
                
                # Use utils.format_time for cleaner HH:MM formatting
                start_time = utils.format_time(item['start_min'])
                
                print(f" {start_time} | {bar} {item['name']}")
            else:
                print(f" ❌ {item['name']}: {item['message']}")

def export_to_csv(schedule_data):
    """
    Writes the results to a file compatible with Excel.
    """
    choice = input("\nSave to CSV? (y/n): ")
    if choice.lower() == 'y':
        try:
            with open('my_schedule.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Day', 'Start', 'End', 'Task', 'Note'])
                writer.writerows(schedule_data)
            print("✓ File saved as 'my_schedule.csv'")
        except Exception as e:
            print(f"Error saving file: {e}")