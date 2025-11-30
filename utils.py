"""
UTILS.PY
--------
Helper functions for time conversion and math.
"""
from constants import MINUTES_PER_DAY

def parse_time(time_str):
    """Converts '14:30' -> 870 minutes."""
    if not time_str or str(time_str).lower() == 'none':
        return None
    try:
        hours, mins = time_str.split(':')
        return int(hours) * 60 + int(mins)
    except ValueError:
        return None

def parse_duration(s):
    """
    Parses '90', '90m', '1.5h' into minutes.
    Complex formats like '1h 30m' are removed to save space.
    """
    if not s: return 0
    s = str(s).lower().strip()
    
    try:
        if s.endswith('h'):
            return int(float(s[:-1]) * 60)  # "1.5h" -> 90
        if s.endswith('m'):
            return int(float(s[:-1]))       # "90m" -> 90
        
        # If just a number: 1.5 -> 90 mins, 90 -> 90 mins
        val = float(s)
        return int(val * 60) if '.' in s else int(val)
    except ValueError:
        return 0

def format_time(minutes):
    """Converts 90 -> '01:30'."""
    if minutes is None: return ""
    hours, mins = divmod(int(minutes) % MINUTES_PER_DAY, 60)
    return f"{hours:02d}:{mins:02d}"

def calculate_recurring_days(freq, min_gap):
    """Returns day indices (1-7) for a recurring task."""
    if freq <= 0: return []
    if freq == 1: return [4]  # Thursday
    
    days = []
    current = 1
    for _ in range(freq):
        days.append(current)
        current += min_gap + 1
    return days

def get_task_flexibility(task):
    """Returns flexibility score (lower is stricter)."""
    return task['latest_min'] - task['earliest_min'] - task['duration']