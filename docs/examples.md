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
1. EXISTING TASK (Scheduled first):
   Name: Staff Meeting
   Duration: 2h
   Time: 09:00 - 11:00
   Priority: S

2. NEW TASK (The Conflict):
   Name: Deep Work
   Duration: 3h
   Earliest Start: 09:00
   Latest End: 12:00
```

**Output:**
```text
❌ Deep Work: TIME CONFLICT! Try: 11:00-14:00
```