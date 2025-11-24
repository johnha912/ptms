import scheduler
import io_handler
import utils
from constants import SLOTS_PER_DAY, PRIORITY_VALUES

# ==========================================
# DEFINING THE DATA (Raw Strings)
# ==========================================

raw_scenario_1 = [
    {'name': 'CS5002 Study Session', 'dur': '2hr', 'start': '09:00', 'end': '18:00', 'freq': 3, 'gap': 1, 'days': [], 'prio': 'A'},
    {'name': 'CS5001 Assignment', 'dur': '3hr', 'start': '10:00', 'end': '20:00', 'freq': 2, 'gap': 2, 'days': [], 'prio': 'S'},
    {'name': 'Gym Workout', 'dur': '1hr30m', 'start': '06:00', 'end': '21:00', 'freq': 4, 'gap': 1, 'days': [], 'prio': 'B'},
    {'name': 'Meal Prep', 'dur': '2hr', 'start': '10:00', 'end': '16:00', 'freq': 1, 'gap': 0, 'days': ['Sunday'], 'prio': 'B'},
    {'name': 'Part-time Job', 'dur': '4hr', 'start': '14:00', 'end': '22:00', 'freq': 3, 'gap': 1, 'days': [], 'prio': 'S'},
    {'name': 'Reading for Fun', 'dur': '1hr', 'start': '19:00', 'end': '23:00', 'freq': 5, 'gap': 0, 'days': [], 'prio': 'F'},
    {'name': 'Video Call Family', 'dur': '45m', 'start': '18:00', 'end': '21:00', 'freq': 1, 'gap': 0, 'days': ['Sunday'], 'prio': 'A'}
]

raw_scenario_2 = [
    {'name': 'Morning Meditation', 'dur': '30m', 'start': '06:00', 'end': '08:00', 'freq': 5, 'gap': 0, 'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'prio': 'A'},
    {'name': 'Deep Work Session', 'dur': '3hr', 'start': '09:00', 'end': '17:00', 'freq': 5, 'gap': 0, 'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'prio': 'S'},
    {'name': 'Team Meetings', 'dur': '1hr30m', 'start': '13:00', 'end': '17:00', 'freq': 3, 'gap': 1, 'days': ['Monday', 'Wednesday', 'Friday'], 'prio': 'S'},
    {'name': 'Lunch Break', 'dur': '1hr', 'start': '11:30', 'end': '13:30', 'freq': 5, 'gap': 0, 'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'prio': 'A'},
    {'name': 'Evening Exercise', 'dur': '1hr', 'start': '17:00', 'end': '20:00', 'freq': 4, 'gap': 1, 'days': [], 'prio': 'B'},
    {'name': 'Side Project', 'dur': '2hr', 'start': '19:00', 'end': '23:00', 'freq': 3, 'gap': 1, 'days': [], 'prio': 'C'},
    {'name': 'Grocery Shopping', 'dur': '1hr30m', 'start': '09:00', 'end': '20:00', 'freq': 1, 'gap': 0, 'days': ['Saturday'], 'prio': 'B'},
    {'name': 'Weekend Hobby', 'dur': '2hr30m', 'start': '10:00', 'end': '18:00', 'freq': 1, 'gap': 0, 'days': ['Sunday'], 'prio': 'C'},
    {'name': 'Social Plans', 'dur': '3hr', 'start': '18:00', 'end': '23:00', 'freq': 1, 'gap': 0, 'days': ['Saturday'], 'prio': 'B'}
]

def clean_data(raw_list):
    """Converts raw strings to integer minutes used by scheduler"""
    clean_tasks = []
    for t in raw_list:
        clean_tasks.append({
            'name': t['name'],
            'duration': utils.parse_duration(t['dur']),
            'earliest_min': utils.parse_time(t['start']),
            'latest_min': utils.parse_time(t['end']),
            'frequency': t['freq'],
            'min_days_between': t['gap'],
            'preferred_days': t['days'],
            'priority': t['prio']
        })
    return clean_tasks

def run_test(name, raw_data):
    print("\n" + "="*60)
    print(f"RUNNING: {name}")
    print("="*60)
    
    # 1. Prepare Data
    tasks = clean_data(raw_data)
    daily_tasks, week_dates = scheduler.assign_tasks_to_days(tasks)
    
    occupied_weekly = [[False] * SLOTS_PER_DAY for _ in range(7)]
    viz_data = [[] for _ in range(7)]
    
    # 2. Schedule
    for day_idx, tasks_on_day in enumerate(daily_tasks):
        if not tasks_on_day: continue
        
        day_name = week_dates[day_idx].strftime("%A")
        print(f"\n--- {day_name} ---")
        
        # Sort Priority S -> F, then by Tightness
        tasks_on_day.sort(key=lambda t: (PRIORITY_VALUES[t['priority']], utils.get_task_flexibility(t)))
        
        for task in tasks_on_day:
            # FIX IS HERE: Added '_' to capture the CSV data we don't need right now
            success, _, viz_entry, msgs = scheduler.try_schedule_task(
                task, day_idx, occupied_weekly, day_name
            )
            for m in msgs: print(m)
            viz_data[day_idx].append(viz_entry)
            
    # 3. Visualize
    io_handler.visualize_schedule(viz_data, week_dates)

if __name__ == "__main__":
    run_test("SCENARIO 1: BUSY STUDENT", raw_scenario_1)
    run_test("SCENARIO 2: WORK-LIFE BALANCE", raw_scenario_2)