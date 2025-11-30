"""
REPORTER.PY
-----------
Handles visual output (ASCII charts) and file saving.
"""
import csv
import utils

def visualize_schedule(viz_data, week_dates):
    """Prints a visual ASCII bar chart of the week."""
    print("\n" + "=" * 60 + "\nSCHEDULE VISUALIZATION\n" + "=" * 60)

    for i, items in enumerate(viz_data):
        if not items: continue
        day_name = week_dates[i].strftime("%A, %b %d")
        print(f"\n{day_name}\n" + "-" * 60)

        # Sort tasks by time
        sorted_items = sorted(items, key=lambda x: x.get('start_min', 9999))

        for item in sorted_items:
            if 'start_min' in item:
                # Calculate bar length: 1 char per 15 mins
                bar_len = item['duration'] // 15
                bar = "█" * min(bar_len, 40) 
                s_time = utils.format_time(item['start_min'])
                print(f" {s_time} | {bar} {item['name']}")
            else:
                print(f" ❌ {item['name']}: {item['message']}")

def export_to_csv(schedule_data):
    """Writes the results to 'my_schedule.csv'."""
    choice = input("\nSave to CSV? (y/n): ")
    if choice.lower() == 'y':
        try:
            with open('my_schedule.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Day', 'Start', 'End', 'Task', 'Note'])
                writer.writerows(schedule_data)
            print("✓ File saved as 'my_schedule.csv'")
        except Exception as e:
            print(f"Error saving file: {e}")