"""
TEST_SCENARIOS.PY
-----------------
Runs scenarios to verify stability.
"""
import scheduler
import reporter
import utils
import test_data
from constants import SLOTS_PER_DAY, PRIORITY_VALUES

def clean_data(raw_data):
    """Converts short-hand data into full task dictionaries."""
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

def run_test(name, raw_data):
    print(f"\n\n{'='*60}\nSCENARIO: {name}\n{'='*60}")
    
    tasks = clean_data(raw_data)
    daily, dates = scheduler.assign_tasks_to_days(tasks)
    occupied = [[False] * SLOTS_PER_DAY for _ in range(7)]
    viz_data = [[] for _ in range(7)]

    for i, day_tasks in enumerate(daily):
        if not day_tasks: continue
        day_name = dates[i].strftime("%A")
        
        # Sort: Critical (S) first, then by tightness
        day_tasks.sort(key=lambda t: (
            PRIORITY_VALUES[t['priority']], utils.get_task_flexibility(t)))

        for task in day_tasks:
            success, _, viz, _ = scheduler.try_schedule_task(
                task, i, occupied, day_name)
            viz_data[i].append(viz)

    reporter.visualize_schedule(viz_data, dates)

if __name__ == "__main__":
    run_test("1: Busy College Student", test_data.COLLEGE_SCENARIO)
    run_test("2: Work-Life Professional", test_data.WORK_SCENARIO)