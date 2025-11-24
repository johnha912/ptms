# 🏗️ Project Design

This document explains how each Python file contributes to the project.

---

## 📁 1. File Responsibilities

### `main.py`
- The “manager” of the whole program  
- Calls input → scheduling → output  
- Runs the day-by-day scheduling loop

### `scheduler.py`
- The “brain”  
- Checks whether slots are free  
- Schedules tasks  
- Suggests alternatives if a task doesn’t fit  
- Handles break insertion for long tasks

### `io_handler.py`
- Talks to the user  
- Asks for task information  
- Prints the ASCII weekly schedule  
- Saves CSV output

### `utils.py`
- Converts “1h30m” → minutes  
- Converts “09:45” → minutes  
- Computes weekly recurring patterns  
- General helper functions

### `constants.py`
- Stores numbers used across the project  
- Easy place to change slot size, priority mapping, etc.

### `test_scenarios.py`
- Automatically runs the scheduler with sample data  
- Useful for debugging and demos

---

## 📚 2. Why the Project Is Split into Multiple Files

Splitting the work helps with:

- easier debugging  
- cleaner organization  
- reusable functions  
- easier final code review  
- easier team collaboration  

It also follows the “Separation of Concerns” principle, which simply means:

> Every file should do one job.

---

## 📦 3. Data Structures

### Task (dictionary)
```python
{
name: "Gym",
duration: 90,
earliest_min: 360,
latest_min: 1320,
frequency: 3,
preferred_days: [],
priority: "A"
}
```

### Daily Task List
```python
daily_tasks = [
[task1, task2], # Monday
[], # Tuesday
...
]
```


### Occupied Slots
```python
occupied = [False] * 96
```

---

## ✔ Summary
The design is simple, modular, and easy for beginners to navigate.
