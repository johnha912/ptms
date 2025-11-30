"""
SCHEDULER.PY
------------
The 'Brain'. Assigns tasks to days and times.
"""
import math
from datetime import date, timedelta
import utils
import recommender
from constants import SLOT_DURATION, SLOTS_PER_DAY

def slots_available(occupied_list, start, end):
    if start < 0 or end >= len(occupied_list): return False
    for k in range(start, end + 1):
        if occupied_list[k] is True: return False 
    return True

def assign_tasks_to_days(tasks):
    start_date = date.today() + timedelta(days=1)
    week_dates = [start_date + timedelta(days=i) for i in range(7)]
    daily_tasks = [[] for _ in range(7)]

    for task in tasks:
        day_indices = []
        if task['preferred_days']:
            for pref_day in task['preferred_days']:
                for i, d in enumerate(week_dates):
                    if d.strftime("%A") == pref_day: day_indices.append(i)
        else:
            rel_days = utils.calculate_recurring_days(task['frequency'], 0)
            day_indices = [d - 1 for d in rel_days]

        for idx in day_indices:
            if 0 <= idx < 7: daily_tasks[idx].append(task)
    return daily_tasks, week_dates

def try_schedule_task(task, day_idx, occupied_weekly, day_name):
    occ = occupied_weekly[day_idx]
    slots = math.ceil(task['duration'] / SLOT_DURATION)
    min_s = math.ceil(task['earliest_min'] / SLOT_DURATION)
    max_s = math.floor(task['latest_min'] / SLOT_DURATION) - slots

    for start in range(min_s, max_s + 1):
        if slots_available(occ, start, start + slots - 1):
            for k in range(start, start + slots): occ[k] = True
            
            s_str = utils.format_time(start * SLOT_DURATION)
            e_str = utils.format_time((start + slots) * SLOT_DURATION)
            
            csv_row = [day_name, s_str, e_str, task['name'], '']
            viz = {'name': task['name'], 'start_min': start * 15, 'duration': task['duration']}
            return (True, csv_row, viz, [])

    # === CONFLICT HANDLING ===
    alts = recommender.find_alternatives(task, occ)
    # Clearer error message for the user
    msg = f"TIME CONFLICT! Try: {', '.join(alts)}" if alts else "DAY FULL"
    
    return (False, [day_name, 'ERR', 'ERR', task['name'], msg], 
            {'name': task['name'], 'message': msg}, [])