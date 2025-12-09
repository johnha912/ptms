"""
TEST_PROJECT.PY
---------------
Unit tests using pytest (Functions + Assert).
Sorted from Simple -> Complex.
Please run with: python -m pytest unit_test.py (from the folder containing this file)
"""
import utils
import recommender
import scheduler
from constants import SLOTS_PER_DAY

# =================================================================
# 1. SIMPLEST: UTILS (Math & Conversions)
# =================================================================

def test_utils_time_conversion():
    """Test converting HH:MM to minutes and back."""
    # Test parse_time
    assert utils.parse_time("01:00") == 60
    assert utils.parse_time("00:00") == 0
    assert utils.parse_time(None) is None
    
    # Test format_time
    assert utils.format_time(60) == "01:00"
    assert utils.format_time(90) == "01:30"

def test_utils_duration():
    """Test parsing duration strings like '90m' or '1.5h'."""
    assert utils.parse_duration("30") == 30
    assert utils.parse_duration("1h") == 60
    assert utils.parse_duration("1.5h") == 90
    assert utils.parse_duration("45m") == 45

def test_utils_recurring_logic():
    """Test the day calculation logic."""
    # Freq=1 should return Thursday (Index 4)
    assert utils.calculate_recurring_days(1, 0) == [4]
    # Freq=3, Gap=1 (skip 1 day) -> Days 1, 3, 5
    assert utils.calculate_recurring_days(3, 1) == [1, 3, 5]

# =================================================================
# 2. MEDIUM: RECOMMENDER (List Logic)
# =================================================================

def test_find_alternatives():
    """Check if the recommender finds a gap in a schedule."""
    # Create a hypothetical day where everything is BUSY (True)
    occupied = [True] * SLOTS_PER_DAY
    
    # Open a gap: 01:00 to 02:00 (4 slots)
    # Slot 4 is 01:00. Slot 8 is 02:00.
    for i in range(4, 8):
        occupied[i] = False
        
    # We need a task that is 60 mins long (4 slots)
    task = {'duration': 60}
    
    # Run the function
    suggestions = recommender.find_alternatives(task, occupied)
    
    # It should find the gap "01:00-02:00"
    assert "01:00-02:00" in suggestions

# =================================================================
# 3. COMPLEX: SCHEDULER (State Changes)
# =================================================================

def test_slots_available():
    """Check the collision detection logic."""
    # [Free, Busy, Free]
    occ = [False, True, False]
    
    # Slot 0 is Free -> True
    assert scheduler.slots_available(occ, 0, 0) == True
    # Slot 1 is Busy -> False
    assert scheduler.slots_available(occ, 1, 1) == False
    # Range 0-2 contains a Busy slot -> False
    assert scheduler.slots_available(occ, 0, 2) == False

def test_scheduler_success():
    """Test placing a task on an empty day."""
    # Setup: Empty day (96 slots of False)
    occupied = [False] * SLOTS_PER_DAY
    day_name = "Monday"
    
    # A 30-minute task (2 slots) starting at 09:00 (Slot 36)
    task = {
        'name': 'Test', 'duration': 30,
        'earliest_min': 540, 'latest_min': 600, 'priority': 'A'
    }
    
    # Run the function (Note: occupied_weekly is a list of lists)
    success, csv, viz, _ = scheduler.try_schedule_task(
        task, 0, [occupied], day_name
    )
    
    # 1. Check that it returned True
    assert success == True
    
    # 2. Check that the 'occupied' list was actually modified
    assert occupied[36] == True  # 09:00 slot
    assert occupied[37] == True  # 09:15 slot
    
    # 3. Check the CSV output data
    assert csv[1] == "09:00" # Start Time
    assert csv[2] == "09:30" # End Time

# =================================================================
# RUNNER
# =================================================================
if __name__ == "__main__":
    # This block allows us to run the tests with standard Python
    print("Running Tests...")
    test_utils_time_conversion()
    test_utils_duration()
    test_utils_recurring_logic()
    test_find_alternatives()
    test_slots_available()
    test_scheduler_success()
    print("All tests passed!")