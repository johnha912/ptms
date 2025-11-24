"""
CONSTANTS.PY
------------
This file holds 'Global Constants'. These are values that do not change
while the program is running.

Naming Convention: We use ALL_CAPS for constants so other programmers
know they shouldn't change these variables during execution.
"""

# How many minutes are in a full 24-hour day
MINUTES_PER_DAY = 1440

# The size of one "block" on the schedule (in minutes).
# 15 means we schedule things in 15-minute chunks.
SLOT_DURATION = 15

# Calculate total slots: 1440 / 15 = 96 slots per day
SLOTS_PER_DAY = MINUTES_PER_DAY // SLOT_DURATION

# Mapping priorities to numbers so we can sort them.
# Lower number = Higher priority (gets scheduled first).
PRIORITY_VALUES = {
    'S': 0,  # Critical
    'A': 1,  # High
    'B': 2,  # Medium
    'C': 3,  # Low
    'D': 4,  # Very Low
    'F': 5   # Flexible
}