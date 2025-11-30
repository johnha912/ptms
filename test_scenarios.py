"""
TEST_SCENARIOS.PY
-----------------
Runs multiple scenarios to verify system stability and error handling.
"""
import scheduler
import reporter
import utils
import test_data
from constants import SLOTS_PER_DAY, PRIORITY_VALUES

def clean_data(raw_data):
    """Converts the short-hand test data into full task dictionaries."""
    tasks = []
    for t in raw_data:
        tasks.append({
            'name': t['name'],
            'duration': utils.parse_duration(t['dur']),
            'earliest_min': utils.parse_time(t['start']),
            'latest_min': utils.parse_time(t['end']),
            'frequency': t['freq'],
            'min_days_between': 0,
            'preferred_days': t['days'],
            'priority': t['prio']
        })
    return tasks

def run_test(scenario_name, raw_data):
    print(f"\n\n{'#'*60}\nTEST SCENARIO: {scenario_name}\n{'#'*60}")
    
    tasks = clean_data(raw_data)
    daily_tasks, week_dates = scheduler.assign_tasks_to_days(tasks)
    occupied = [[False] * SLOTS_PER_DAY for _ in range(7)]
    viz_data = [[] for _ in range(7)]

    for i, day_tasks in enumerate(daily_tasks):
        if not day_tasks: continue
        day_name = week_dates[i].strftime("%A")
        
        # Sort: High priority (S) goes first!
        day_tasks.sort(key=lambda t: (
            PRIORITY_VALUES[t['priority']], utils.get_task_flexibility(t)))

        for task in day_tasks:
            # We ignore csv_entry (_) here
            _, _, viz, _ = scheduler.try_schedule_task(task, i, occupied, day_name)
            viz_data[i].append(viz)

    reporter.visualize_schedule(viz_data, week_dates)

if __name__ == "__main__":
    # 1. Run the Success Case
    run_test("Happy Path (Student)", test_data.STUDENT_SCENARIO)
    
    # 2. Run the Failure/Recommender Case
    run_test("Conflict Path (Recommender)", test_data.CONFLICT_SCENARIO)