# 📅 Passive Time Management Scheduler

> A smart weekly scheduler that fits tasks into your life using a priority-based greedy algorithm.

![Status](https://img.shields.io/badge/Status-Completed-success) ![Python](https://img.shields.io/badge/Python-3.x-blue)

## 📖 Overview
This project is a Python-based application designed to automate weekly planning. Unlike standard calendars where you manually drag-and-drop tasks, this scheduler takes a list of tasks (with constraints like priority, duration, and frequency) and automatically finds the optimal time slots for them.

It features **Conflict Resolution**, **Smart Break Insertion**, and a **Recommender System** that suggests alternative times when a schedule is full.

## 🚀 Key Features
* **Auto-Scheduling:** Assigns 15-minute blocks based on "Earliest Start" and "Latest End" constraints.
* **Priority Logic:** Critical ('S') tasks are scheduled before Flexible ('F') tasks.
* **Smart Breaks:** Automatically inserts a 15-minute break after any task longer than 2 hours.
* **Recovery Mode:** If a task cannot fit, the system scans the day and suggests specific free time windows.
* **Visual Output:** Generates an ASCII bar chart of the week in the console.
* **Data Export:** Saves the final schedule to `my_schedule.csv` for Excel/Google Sheets.

## 🛠️ Project Structure
This project follows a modular architecture to separate business logic from user interaction.

| File | Description |
| :--- | :--- |
| `main.py` | The entry point. Orchestrates the flow between Input, Logic, and Output. |
| `scheduler.py` | The "Brain." Contains the greedy algorithm, collision detection, and recommender logic. |
| `io_handler.py` | Handles all user inputs and draws the ASCII visualization. |
| `utils.py` | Helper functions for time parsing (e.g., converting "14:30" to 870 minutes). |
| `test_scenarios.py` | A test suite with pre-defined scenarios (Student vs. Professional) to demonstrate the logic. |

## 💻 How to Run

### Prerequisites
* Python 3.6 or higher.
* No external libraries required (uses standard `math`, `csv`, `datetime`, `re`).

### Steps
1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/ptms.git](https://github.com/YOUR_USERNAME/ptms.git)
    cd ptms
    ```

2.  **Run the Interactive App**
    ```bash
    python main.py
    ```
    Follow the prompts to enter your tasks. Type `done` when finished.

3.  **Run the Test Scenarios**
    To see the scheduler in action with complex data (without typing it manually):
    ```bash
    python test_scenarios.py
    ```

## 📚 Documentation
For deep technical details, please see the `docs/` folder:
* [**Algorithm Logic**](docs/algorithm_logic.md): Flowcharts explaining the scheduling loop and recommender system.
* [**System Design**](docs/design.md): Explanation of the Separation of Concerns and Data Structures.

## 👤 Author
* Nguyen "John" Ha & Yanglin "Elliot" Hu
* CS5001 Final Project - Professor Mark Miller
* Northeastern University - Fall 2025