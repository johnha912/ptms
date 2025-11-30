"""
RECOMMENDER.PY
--------------
Suggests alternative time slots when the schedule is full.
"""
import math
import utils
from constants import SLOT_DURATION

def find_alternatives(task, occupied):
    """
    Scans the day for free windows that fit the task duration.
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
            # We hit a busy slot, check if previous gap was big enough
            if free_count >= slots_needed:
                _add_suggestion(suggestions, current_start, slots_needed)
            free_count = 0
            
    # Check the very last block of the day
    if free_count >= slots_needed:
        _add_suggestion(suggestions, current_start, slots_needed)
        
    return suggestions[:3] # Return top 3 options only

def _add_suggestion(suggestion_list, start_slot, slots_needed):
    """Helper to format and add a time range string."""
    s_str = utils.format_time(start_slot * SLOT_DURATION)
    e_str = utils.format_time((start_slot + slots_needed) * SLOT_DURATION)
    suggestion_list.append(f"{s_str}-{e_str}")