"""
TEST_DATA.PY
------------
Raw sample data for testing.
Keys: dur=Duration, freq=Frequency, prio=Priority
"""

# SCENARIO 1: BUSY COLLEGE STUDENT
COLLEGE_SCENARIO = [
    {'name': 'CS5002 Study', 'dur': '2h', 'start': '09:00', 'end': '18:00', 'freq': 3, 'days': [], 'prio': 'A'},
    {'name': 'CS5001 Assign', 'dur': '3h', 'start': '10:00', 'end': '20:00', 'freq': 2, 'days': [], 'prio': 'S'},
    {'name': 'Gym Workout', 'dur': '90m', 'start': '06:00', 'end': '21:00', 'freq': 4, 'days': [], 'prio': 'B'},
    {'name': 'Meal Prep', 'dur': '2h', 'start': '10:00', 'end': '16:00', 'freq': 1, 'days': ['Sunday'], 'prio': 'B'},
    {'name': 'Part-time Job', 'dur': '4h', 'start': '14:00', 'end': '22:00', 'freq': 3, 'days': [], 'prio': 'S'},
    {'name': 'Reading', 'dur': '1h', 'start': '19:00', 'end': '23:00', 'freq': 5, 'days': [], 'prio': 'F'},
    {'name': 'Family Call', 'dur': '45m', 'start': '18:00', 'end': '21:00', 'freq': 1, 'days': ['Sunday'], 'prio': 'A'}
]

# SCENARIO 2: WORK-LIFE BALANCE PROFESSIONAL
WORK_SCENARIO = [
    {'name': 'Meditation', 'dur': '30m', 'start': '06:00', 'end': '08:00', 'freq': 5, 'days': ['Monday','Tuesday','Wednesday','Thursday','Friday'], 'prio': 'A'},
    {'name': 'Deep Work', 'dur': '3h', 'start': '09:00', 'end': '17:00', 'freq': 5, 'days': ['Monday','Tuesday','Wednesday','Thursday','Friday'], 'prio': 'S'},
    {'name': 'Team Meeting', 'dur': '90m', 'start': '13:00', 'end': '17:00', 'freq': 3, 'days': ['Monday','Wednesday','Friday'], 'prio': 'S'},
    {'name': 'Lunch Break', 'dur': '1h', 'start': '11:30', 'end': '13:30', 'freq': 5, 'days': ['Monday','Tuesday','Wednesday','Thursday','Friday'], 'prio': 'A'},
    {'name': 'Exercise', 'dur': '1h', 'start': '17:00', 'end': '20:00', 'freq': 4, 'days': [], 'prio': 'B'},
    {'name': 'Side Project', 'dur': '2h', 'start': '19:00', 'end': '23:00', 'freq': 3, 'days': [], 'prio': 'C'},
    {'name': 'Groceries', 'dur': '90m', 'start': '09:00', 'end': '20:00', 'freq': 1, 'days': ['Saturday'], 'prio': 'B'},
    {'name': 'Hobby Time', 'dur': '2.5h', 'start': '10:00', 'end': '18:00', 'freq': 1, 'days': ['Sunday'], 'prio': 'C'},
    {'name': 'Social Plans', 'dur': '3h', 'start': '18:00', 'end': '23:00', 'freq': 1, 'days': ['Saturday'], 'prio': 'B'}
]