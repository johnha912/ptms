# 📘 Project Documentation — Overview

This folder provides simple, beginner-friendly explanations of how the Passive Time Management Scheduler works.
It is meant for CS5001 Align students who want to understand the project structure without diving into advanced algorithms.

---

## ⭐ What This Scheduler Does
The program helps you automatically place your weekly tasks into a schedule.
Instead of dragging items around on a calendar, you tell the program:

- how long a task takes
- when it can start
- when it must finish
- how many times per week it happens
- its priority

… and the program finds the best available time slot for you.

When it cannot fit a task, it will suggest alternative free windows.

---

## ⭐ What’s Inside the Docs
| File | Purpose |
|------|---------|
| `overview.md` | Big-picture explanation of the project |
| `algorithm.md` | Simple explanation of the scheduling logic |
| `design.md` | How the files in the project work together |
| `examples.md` | Sample outputs and scenarios |

---

## ⭐ Where the Main Code Lives
The project is split into small files so each one is easy to read:

- `main.py` — runs the whole program
- `scheduler.py` — finds time slots for tasks (The "Brain")
- `recommender.py` — suggests times if the schedule is full (The "Advisor")
- `io_handler.py` — gets user input
- `reporter.py` — draws the chart and saves the CSV
- `utils.py` — time parsing and helper functions
- `test_scenarios.py` — pre-built examples