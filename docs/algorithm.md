# 🧠 How the Scheduling Algorithm Works

This is a beginner-friendly explanation of how tasks are placed into your weekly schedule.

---

## 1. Task Preparation
Before scheduling, each task is converted into simple numbers (minutes) using `utils.py`.
- "09:00" becomes `540`
- "1h 30m" becomes `90`

---

## 2. Sorting Tasks by Priority
Before scheduling each day, `main.py` sorts the tasks:

1. Critical tasks (S) first
2. High priority (A)
3. Medium (B)
4. Low (C, D, F)

If two tasks have the same priority, the one with less time flexibility goes first.

---

## 3. Placing Tasks Into Time Slots (`scheduler.py`)
Each day has 96 slots (15 minutes each).
The scheduler checks each possible start time:

```pseudo
start = earliest_possible
while start <= latest_possible:
    if the block is free:
        schedule the task here
        STOP and return Success
```

## 4. If Scheduling Fails (`recommender.py`)
If a task cannot fit between its earliest start and latest end, the **Recommender** takes over.

**The Logic:**
1. It ignores the "earliest/latest" constraints.
2. It searches the entire day for any open gap that is long enough.
3. It returns the top 3 options to the user.

Example message: *"Conflict! We couldn't fit 'Gym' at your preferred time. But 14:00-15:30 is free."*
