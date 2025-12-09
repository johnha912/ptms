# 📅 Passive Time Management Scheduler

> A smart weekly scheduler that fits tasks into your life using a priority-based greedy algorithm.

## 📖 Overview
This project is a Python-based application designed to automate weekly planning. Unlike standard calendars where you manually drag-and-drop tasks, this scheduler takes a list of tasks (with constraints like priority, duration, and frequency) and automatically finds the optimal time slots for them.

It features **Conflict Resolution** and a **Recommender System** that suggests alternative times when a schedule is full.

## 🚀 Key Features
* **Auto-Scheduling:** Assigns 15-minute blocks based on "Earliest Start" and "Latest End" constraints.
* **Priority Logic:** Critical ('S') tasks are scheduled before Flexible ('C') tasks.
* **Conflict Handling:** If a task doesn't fit, the system detects the error.
* **Recommender System:** Scans the day for free gaps and suggests specific alternative times (e.g., *"Try 14:00-16:00"*).
* **Visual Output:** Generates an ASCII bar chart of the week in the console.
* **Data Export:** Saves the final schedule to `my_schedule.csv`.

## 🛠️ Project Structure
The code is split into small, focused modules (under 75 lines each) to ensure readability and easy debugging.

| File | Role | Description |
| :--- | :--- | :--- |
| `main.py` | **Entry** | The manager. Orchestrates the flow between modules. |
| `scheduler.py` | **Logic** | The "Brain." Decides where tasks go using a simple algorithm. |
| `recommender.py` | **Logic** | The "Advisor." Finds alternative slots when conflicts occur. |
| `io_handler.py` | **Input** | Handles user prompts to collect task data. |
| `reporter.py` | **Output** | Handles ASCII visualization and CSV file saving. |
| `utils.py` | **Helper** | specific math and time conversion functions. |
| `test_scenarios.py` | **Test** | Runs automated tests (Success and Conflict scenarios). |
| `test_data.py` | **Data** | Holds raw data for testing so the logic stays clean. |

## 💻 How to Run

### Prerequisites
* Python 3.6 or higher.
* No external libraries required (uses standard `math`, `csv`, `datetime`).

### 1. Interactive Mode (User Input)
Run the main program to enter your own tasks:
```bash
python main.py
```
Follow the prompts. Type done when finished adding tasks.

### 2. Test Mode (Automated)
Run the test suite to see how the system handles complex scenarios:
```bash
python test_scenarios.py
```
This will run two scenarios:

1. **Busy College Student**: A high-intensity schedule with classes, jobs, and study.

2. **Work-Life Professional**: A structured week with meetings, deep work, and hobbies.

# 📚 Documentation

For deep technical details, please see the docs/ folder:

* [Overview](docs/overview.md): High-level summary for beginners.
* [Algorithm](docs/algorithm.md): How the scheduling logic works.
* [System Design](docs/design.md): Explanation of the modular architecture.
* [Examples](docs/examples.md): Sample outputs and scenarios.

# 👤 Author
* Nguyen "John" Ha & Yanglin "Elliot" Hu
* CS5001 Final Project - Professor Mark Miller
* Northeastern University - Fall 2025
