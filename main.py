"""
MAIN.PY
-------
Entry point. Imports functionality from modular files.
"""
import scheduler
import io_handler
import reporter
import utils
from constants import SLOTS_PER_DAY, PRIORITY_VALUES

def main():
    print("Welcome to the Python Weekly Scheduler")
    
    # 1. GET INPUTS
    tasks = io_handler.get_tasks_from_user()
    if not tasks: return

    # 2. PREPARE DATA
    daily_tasks, week_dates = scheduler.assign_tasks_to_days(tasks)

    # 3. RUN SCHEDULING ALGORITHM
    print("\nGenerating Schedule...")
    occupied_weekly = [[False] * SLOTS_PER_DAY for _ in range(7)]
    
    all_schedule_entries = []
    visualization_data = [[] for _ in range(7)]

    for day_idx, tasks_on_day in enumerate(daily_tasks):
        day_name = week_dates[day_idx].strftime("%A")
        
        if not tasks_on_day:
            continue
        
        # Sort tasks: Critical (S) first, then by tightness
        tasks_on_day.sort(key=lambda t: (
            PRIORITY_VALUES[t['priority']], utils.get_task_flexibility(t)))

        for task in tasks_on_day:
            success, csv_entry, viz_entry, logs = scheduler.try_schedule_task(
                task, day_idx, occupied_weekly, day_name
            )
            all_schedule_entries.append(csv_entry)
            visualization_data[day_idx].append(viz_entry)

    # 4. OUTPUT RESULTS (Using the new reporter module)
    reporter.visualize_schedule(visualization_data, week_dates)
    reporter.export_to_csv(all_schedule_entries)

if __name__ == "__main__":
    main()