"""
SCHEDULER.PY
------------
The 'Brain' of the application.
Includes conflict detection and the new RECOMMENDER SYSTEM.
"""

import math
from datetime import date, timedelta
import utils
from constants import SLOT_DURATION, MINUTES_PER_DAY, SLOTS_PER_DAY

# ================= HELPER LOGIC =================

def slots_available(occupied_list, start_index, end_index):
    if start_index < 0 or end_index >= len(occupied_list):
        return False
    for k in range(start_index, end_index + 1):
        if occupied_list[k] is True:
            return False 
    return True

def occupy_slots(occupied_list, start_index, end_index):
    for k in range(start_index, end_index + 1):
        if 0 <= k < len(occupied_list):
            occupied_list[k] = True

def find_alternatives(task, occupied):
    """
    NEW FEATURE: Recommender System.
    Scans the day for any free windows that fit the task duration.
    Returns a list of strings like "14:00-16:00".
    """
    slots_needed = math.ceil(task['duration'] / SLOT_DURATION)
    suggestions = []
    
    current_start = 0
    free_count = 0
    
    # Scan every slot in the day (0 to 95)
    for i, is_busy in enumerate(occupied):
        if not is_busy:
            if free_count == 0:
                current_start = i
            free_count += 1
        else:
            # We hit a busy slot, check if the previous gap was big enough
            if free_count >= slots_needed:
                start_str = utils.format_time(current_start * SLOT_DURATION)
                end_str = utils.format_time((current_start + slots_needed) * SLOT_DURATION)
                suggestions.append(f"{start_str}-{end_str}")
            
            # Reset counter
            free_count = 0
            
    # Check the very last block of the day (edge case)
    if free_count >= slots_needed:
        start_str = utils.format_time(current_start * SLOT_DURATION)
        end_str = utils.format_time((current_start + slots_needed) * SLOT_DURATION)
        suggestions.append(f"{start_str}-{end_str}")
        
    return suggestions[:3] # Return top 3 options only

# ================= MAIN FUNCTIONS =================

def assign_tasks_to_days(tasks):
    start_date = date.today() + timedelta(days=1)
    week_dates = [start_date + timedelta(days=i) for i in range(7)]
    daily_tasks = [[] for _ in range(7)]

    for task in tasks:
        day_indices = []
        if task['preferred_days']:
            for pref_day in task['preferred_days']:
                for i, d in enumerate(week_dates):
                    if d.strftime("%A") == pref_day:
                        day_indices.append(i)
        else:
            relative_days = utils.calculate_recurring_days(task['frequency'], task['min_days_between'])
            day_indices = [d - 1 for d in relative_days]

        for idx in day_indices:
            if 0 <= idx < 7:
                daily_tasks[idx].append(task)

    return daily_tasks, week_dates

def try_schedule_task(task, day_idx, occupied_weekly, day_name):
    occupied = occupied_weekly[day_idx]
    slots_needed = math.ceil(task['duration'] / SLOT_DURATION)
    
    min_start_slot = math.ceil(task['earliest_min'] / SLOT_DURATION)
    max_start_slot = math.floor(task['latest_min'] / SLOT_DURATION) - slots_needed

    # 1. Try to schedule normally
    for start_slot in range(min_start_slot, max_start_slot + 1):
        end_slot = start_slot + slots_needed - 1
        
        if slots_available(occupied, start_slot, end_slot):
            occupy_slots(occupied, start_slot, end_slot)
            
            start_str = utils.format_time(start_slot * SLOT_DURATION)
            end_str = utils.format_time((end_slot + 1) * SLOT_DURATION)
            
            schedule_entry = [day_name, start_str, end_str, task['name'], '']
            viz_entry = {
                'name': task['name'], 'start_min': start_slot * SLOT_DURATION,
                'end_str': end_str, 'duration': task['duration'], 'priority': task['priority']
            }
            return (True, schedule_entry, viz_entry, [f"  Scheduled: {start_str}-{end_str}"])

    # 2. FAILURE handling with RECOMMENDER
    msg = f"⚠️ Conflict: No space for '{task['name']}'"
    messages = [f"  {msg}"]
    
    # --- CALL THE NEW FUNCTION HERE ---
    alternatives = find_alternatives(task, occupied)
    
    if alternatives:
        rec_msg = "    💡 Try: " + ", ".join(alternatives)
        messages.append(rec_msg)
        msg += f" (Try: {alternatives[0]})"
    else:
        messages.append("    🔴 Day is completely full!")
        
    schedule_entry = [day_name, 'ERR', 'ERR', task['name'], msg]
    viz_entry = {'name': task['name'], 'message': msg}
    
    return (False, schedule_entry, viz_entry, messages)