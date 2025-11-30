# 📝 Examples & Sample Outputs

This document shows what the scheduler looks like when running.

---

## Example 1 — Simple 1-Day Scheduling

**Input:**
```text
Task name: Study
Duration: 2h
Earliest Start: 09:00
Latest End: 14:00
Priority: A
```

**Output:**
```text
Monday, Dec 01
------------------------------------------------------------
 09:00 | ████████ Study
 ```

## Example 2 — When a Task Doesn't Fit
**Input:**
```text
Task: Deep Work
Duration: 3h
Earliest Start: 09:00
Latest End: 11:00
```

**Output:**
```text
❌ Deep Work: TIME CONFLICT! Try: 11:00-14:00
```

## Example 3 — Full Student Scenario
Using `test_scenarios.py`.

You will see sections like:
```text
Monday, Dec 01
------------------------------------------------------------
 06:00 | ████ Gym Workout
 10:00 | ████████████ CS5001 Assignment
 15:00 | ████████ CS5002 Study Session

Sunday, Dec 07
------------------------------------------------------------
 10:00 | ████████ Meal Prep
 19:00 | ██ Video Call
```