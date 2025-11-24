"""
MAIN.PY
-------
This is the entry point. Run this file to start the program.
It imports functionality from the other 3 modules.
"""

# Import our custom modules
import scheduler
import io_handler
import utils
from constants import SLOTS_PER_DAY, PRIORITY_VALUES

def main():
    print("Welcome to the Python Weekly Scheduler")
    
    # 1. GET INPUTS
    # We call the IO handler to talk to the user
    tasks = io_handler.get_tasks_from_user()
    
    if not tasks:
        print("No tasks entered. Exiting.")
        return

    # 2. PREPARE DATA
    # Assign tasks to specific days (logic)
    daily_tasks, week_dates = scheduler.assign_tasks_to_days(tasks)

    # 3. RUN SCHEDULING ALGORITHM
    print("\nGenerating Schedule...")
    
    # Create a 7-day list of empty booleans [False, False...]
    occupied_weekly = [[False] * SLOTS_PER_DAY for _ in range(7)]
    
    all_schedule_entries = []
    visualization_data = [[] for _ in range(7)]

    # Loop through each day
    for day_idx, tasks_on_day in enumerate(daily_tasks):
        if not tasks_on_day: continue

        day_name = week_dates[day_idx].strftime("%A")
        
        # Sort tasks: Critical (S) first, then by tightness of flexibility
        tasks_on_day.sort(key=lambda t: (
            PRIORITY_VALUES[t['priority']], 
            utils.get_task_flexibility(t)
        ))

        for task in tasks_on_day:
            # Call the scheduler logic for this single task
            success, csv_entry, viz_entry, logs = scheduler.try_schedule_task(
                task, day_idx, occupied_weekly, day_name
            )
            
            # Save results
            all_schedule_entries.append(csv_entry)
            visualization_data[day_idx].append(viz_entry)
            
            # Print logs if needed (optional)
            # for log in logs: print(log)

    # 4. OUTPUT RESULTS
    io_handler.print_visualization(visualization_data, week_dates)
    io_handler.export_to_csv(all_schedule_entries)

# Standard Python check: only run main() if this file is executed directly
if __name__ == "__main__":
    main()