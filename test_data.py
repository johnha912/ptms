"""
TEST_DATA.PY
------------
Contains raw sample data for testing purposes.
"""

# SCENARIO 1: The "Happy Path" (Everything should fit)
STUDENT_SCENARIO = [
    {'name': 'CS5002 Study', 'dur': '2h', 'start': '09:00', 'end': '18:00', 
     'freq': 3, 'days': [], 'prio': 'A'},
    {'name': 'Gym', 'dur': '1h', 'start': '06:00', 'end': '21:00', 
     'freq': 4, 'days': [], 'prio': 'B'},
    {'name': 'Job', 'dur': '4h', 'start': '14:00', 'end': '22:00', 
     'freq': 3, 'days': [], 'prio': 'S'}
]

# SCENARIO 2: The "Conflict Path" (Forces a collision)
# 'Final Exam' (S) takes 13:00-17:00.
# 'Party' (C) wants 14:00-16:00. It CANNOT fit.
CONFLICT_SCENARIO = [
    {'name': 'Final Exam', 'dur': '4h', 'start': '13:00', 'end': '17:00', 
     'freq': 1, 'days': ['Monday'], 'prio': 'S'},
    
    {'name': 'Pizza Party', 'dur': '2h', 'start': '14:00', 'end': '16:00', 
     'freq': 1, 'days': ['Monday'], 'prio': 'C'}
]