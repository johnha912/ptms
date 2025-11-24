# 📝 Examples & Sample Outputs

This document shows what the scheduler looks like when running.

---

## Example 1 — Simple 1-Day Scheduling

Input:
```pseudo
Task name: Study
Duration: 2h
Earliest Start: 09:00
Latest End: 14:00
Priority: A
```

Output:
```
Monday
09:00 | █████████████████████ Study
```


---

## Example 2 — When a Task Doesn't Fit

Input:
```pseudo
Task: Deep Work
Duration: 3h
Earliest Start: 09:00
Latest End: 11:00
```


Output:
```pseudo
❌ Deep Work: No space between your earliest and latest time.
💡 Try: 11:00-14:00
```


---

## Example 3 — Full Student Scenario
Using `test_scenarios.py`.

You will see sections like:

```pseudo
Monday
06:00 | ████ Gym Workout
10:00 | █████████ CS5001 Assignment
15:00 | ██████████████ CS5002 Study Session

Sunday
10:00 | ███████ Meal Prep
19:00 | ███ Video Call Family
```


---

## Example 4 — CSV Output

Example row in `my_schedule.csv`:

```pseudo
Monday,09:00,11:00,CS5001 Assignment,
```
These examples should help new users understand what to expect.
