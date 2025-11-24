"""
UTILS.PY
--------
Utilities and Helper Functions.
These functions handle raw data conversion (like string to time).
They do not know about the 'schedule' or 'tasks', they just do math.
"""

import re
import math
from constants import MINUTES_PER_DAY

def parse_time(time_str):
    """
    Converts a string like '14:30' into minutes since midnight.
    Example: '01:00' -> 60
    """
    # Check if string is empty or 'none'
    if not time_str or str(time_str).lower() == 'none':
        return None
    
    try:
        # Split "14:30" into [14, 30]
        parts = time_str.split(':')
        hours = int(parts[0])
        mins = int(parts[1])
        return hours * 60 + mins
    except ValueError:
        return None

def parse_duration(duration_str):
    """
    Converts strings like '1h 30m', '90', or '1.5' into total minutes.
    """
    if not duration_str:
        return 0
        
    s = str(duration_str).lower()
    
    # Regex explains: Look for digits (\d) followed by 'h' or 'm'
    hour_match = re.search(r'(\d+(?:\.\d+)?)\s*(h|hr|hour|hours)', s)
    min_match = re.search(r'(\d+(?:\.\d+)?)\s*(m|min|minute|minutes)', s)

    hours = float(hour_match.group(1)) if hour_match else 0
    mins = float(min_match.group(1)) if min_match else 0

    # If user just typed a number like "90" or "1.5"
    if not hour_match and not min_match:
        try:
            val = float(s)
            # If it has a decimal (1.5), treat as hours. If integer (90), treat as minutes.
            return int(val * 60) if '.' in s else int(val)
        except ValueError:
            return 0

    return int(hours * 60 + mins)

def format_time(minutes):
    """
    Converts minutes (e.g., 90) back into a string (e.g., "01:30").
    """
    if minutes is None:
        return ""
    # divmod returns both the quotient (hours) and remainder (minutes)
    hours, mins = divmod(int(minutes) % MINUTES_PER_DAY, 60)
    # f"{hours:02d}" ensures we get "09" instead of "9"
    return f"{hours:02d}:{mins:02d}"

def calculate_recurring_days(frequency, min_gap):
    """
    Determines which days a task should happen based on frequency.
    Returns a list of day numbers (1 to 7).
    """
    if frequency <= 0:
        return []
    if frequency == 1:
        return [4]  # If once a week, put it on Thursday (middle)

    # Logic: Start at day 1, add gap, repeat.
    days = [1]
    current = 1
    for _ in range(frequency - 1):
        current += min_gap + 1
        days.append(current)
    return days

def get_task_flexibility(task):
    """
    Calculates how 'tight' a deadline is.
    Formula: (Latest End - Earliest Start) - Duration
    Smaller number = Harder to schedule.
    """
    return task['latest_min'] - task['earliest_min'] - task['duration']