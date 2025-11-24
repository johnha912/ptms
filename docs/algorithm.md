# 🧠 How the Scheduling Algorithm Works (Simple Version)

This is a beginner-friendly explanation of how tasks are placed into your weekly schedule.

---

## 1. Task Preparation
Before scheduling, each task is converted into:

- total duration (in minutes)  
- earliest start time  
- latest end time  
- which day(s) it should happen  
- priority (S, A, B, C, F)  

All of this happens in `utils.py`.

---

## 2. Assign Tasks to Days
Every task needs to be attached to one or more days of the week.

Two possibilities:

### ✔ If the user selected exact days:  
Example: `"Mon, Wed"` → assigned only on Monday and Wednesday.

### ✔ If not:  
The program spreads tasks across the week based on how many times per week they repeat.

This happens in `assign_tasks_to_days()`.

---

## 3. Sorting Tasks by Priority
Before scheduling each day:

1. Critical tasks (S) first  
2. High priority (A)  
3. Medium (B)  
4. Low (C, D, F)  

If two tasks have the same priority, the one with less time flexibility goes first.

Sorting happens in `main.py`.

---

## 4. Placing Tasks Into Time Slots
Each day has 96 slots  
(24 hours × 4 slots per hour since each slot is 15 minutes).

The scheduler checks each possible start time:

```pseudo
start = earliest_possible
while start <= latest_possible:
if the block is free:
schedule the task here
stop
```


This is done in `try_schedule_task()`.

---

## 5. If Scheduling Fails
If a task cannot fit between its earliest start and latest end:

### The program does two things:

1. Marks it as a conflict  
2. Searches the entire day for any open gap that is long enough  

This is the “Recommender System”.

Example message:

```pseudo
⚠️ No space for 'Gym Workout'
💡 Try: 14:00-16:00
```


---

## 6. Output
At the end of the week:

- a text-based schedule appears in the console  
- an optional CSV file is created (`my_schedule.csv`)  

---

## That’s It!
The algorithm is intentionally simple so other beginner students can read, understand, and build on it.
