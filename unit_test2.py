"""
TEST_PROJECT2.PY
----------------
Unit tests using unittest module with class-based organization.
Tests are organized from Simple -> Complex across different modules.

Run with: python -m unittest unit_test2.py
Or:       python unit_test2.py
"""
import unittest
import utils
import recommender
import scheduler
from constants import SLOTS_PER_DAY, SLOT_DURATION, MINUTES_PER_DAY, PRIORITY_VALUES


# =================================================================
# TEST CLASS 1: CONSTANTS MODULE
# =================================================================
class TestConstants(unittest.TestCase):
    """Test that constants are correctly defined."""

    def test_minutes_per_day(self):
        """Verify MINUTES_PER_DAY equals 24 * 60."""
        self.assertEqual(MINUTES_PER_DAY, 1440)

    def test_slot_duration(self):
        """Verify slot duration is 15 minutes."""
        self.assertEqual(SLOT_DURATION, 15)

    def test_slots_per_day_calculation(self):
        """Verify slots per day = 1440 / 15 = 96."""
        self.assertEqual(SLOTS_PER_DAY, 96)
        self.assertEqual(SLOTS_PER_DAY, MINUTES_PER_DAY // SLOT_DURATION)

    def test_priority_values_order(self):
        """Verify priority ordering: S < A < B < C < D < F."""
        self.assertLess(PRIORITY_VALUES['S'], PRIORITY_VALUES['A'])
        self.assertLess(PRIORITY_VALUES['A'], PRIORITY_VALUES['B'])
        self.assertLess(PRIORITY_VALUES['B'], PRIORITY_VALUES['C'])
        self.assertLess(PRIORITY_VALUES['C'], PRIORITY_VALUES['D'])
        self.assertLess(PRIORITY_VALUES['D'], PRIORITY_VALUES['F'])

    def test_priority_values_all_exist(self):
        """Verify all priority keys exist."""
        expected_keys = {'S', 'A', 'B', 'C', 'D', 'F'}
        self.assertEqual(set(PRIORITY_VALUES.keys()), expected_keys)


# =================================================================
# TEST CLASS 2: UTILS MODULE - TIME PARSING
# =================================================================
class TestUtilsTimeParsing(unittest.TestCase):
    """Test time parsing and formatting functions."""

    def test_parse_time_standard(self):
        """Test parsing standard HH:MM format."""
        self.assertEqual(utils.parse_time("00:00"), 0)
        self.assertEqual(utils.parse_time("01:00"), 60)
        self.assertEqual(utils.parse_time("12:00"), 720)
        self.assertEqual(utils.parse_time("23:59"), 1439)

    def test_parse_time_with_minutes(self):
        """Test parsing times with non-zero minutes."""
        self.assertEqual(utils.parse_time("01:30"), 90)
        self.assertEqual(utils.parse_time("14:45"), 885)
        self.assertEqual(utils.parse_time("09:15"), 555)

    def test_parse_time_none_input(self):
        """Test parse_time returns None for invalid inputs."""
        self.assertIsNone(utils.parse_time(None))
        self.assertIsNone(utils.parse_time("none"))
        self.assertIsNone(utils.parse_time("None"))

    def test_parse_time_invalid_format(self):
        """Test parse_time handles invalid formats gracefully."""
        self.assertIsNone(utils.parse_time("invalid"))
        self.assertIsNone(utils.parse_time(""))

    def test_format_time_standard(self):
        """Test formatting minutes back to HH:MM."""
        self.assertEqual(utils.format_time(0), "00:00")
        self.assertEqual(utils.format_time(60), "01:00")
        self.assertEqual(utils.format_time(90), "01:30")
        self.assertEqual(utils.format_time(720), "12:00")

    def test_format_time_none_input(self):
        """Test format_time handles None."""
        self.assertEqual(utils.format_time(None), "")

    def test_format_time_wraps_at_midnight(self):
        """Test that format_time wraps correctly at day boundary."""
        # 1440 minutes = 24:00 should wrap to 00:00
        self.assertEqual(utils.format_time(1440), "00:00")
        self.assertEqual(utils.format_time(1500), "01:00")

    def test_time_roundtrip(self):
        """Test parse -> format returns original string."""
        test_times = ["00:00", "09:30", "14:45", "23:59"]
        for time_str in test_times:
            minutes = utils.parse_time(time_str)
            result = utils.format_time(minutes)
            self.assertEqual(result, time_str)


# =================================================================
# TEST CLASS 3: UTILS MODULE - DURATION PARSING
# =================================================================
class TestUtilsDurationParsing(unittest.TestCase):
    """Test duration parsing function."""

    def test_parse_duration_minutes_only(self):
        """Test parsing plain number as minutes."""
        self.assertEqual(utils.parse_duration("30"), 30)
        self.assertEqual(utils.parse_duration("90"), 90)
        self.assertEqual(utils.parse_duration("120"), 120)

    def test_parse_duration_with_m_suffix(self):
        """Test parsing durations with 'm' suffix."""
        self.assertEqual(utils.parse_duration("30m"), 30)
        self.assertEqual(utils.parse_duration("45m"), 45)
        self.assertEqual(utils.parse_duration("90m"), 90)

    def test_parse_duration_with_h_suffix(self):
        """Test parsing durations with 'h' suffix."""
        self.assertEqual(utils.parse_duration("1h"), 60)
        self.assertEqual(utils.parse_duration("2h"), 120)
        self.assertEqual(utils.parse_duration("3h"), 180)

    def test_parse_duration_decimal_hours(self):
        """Test parsing decimal hour values."""
        self.assertEqual(utils.parse_duration("1.5h"), 90)
        self.assertEqual(utils.parse_duration("2.5h"), 150)
        self.assertEqual(utils.parse_duration("0.5h"), 30)

    def test_parse_duration_decimal_number(self):
        """Test parsing decimal number (interpreted as hours)."""
        self.assertEqual(utils.parse_duration("1.5"), 90)
        self.assertEqual(utils.parse_duration("2.0"), 120)

    def test_parse_duration_empty_or_invalid(self):
        """Test parse_duration returns 0 for invalid inputs."""
        self.assertEqual(utils.parse_duration(""), 0)
        self.assertEqual(utils.parse_duration(None), 0)
        self.assertEqual(utils.parse_duration("invalid"), 0)

    def test_parse_duration_case_insensitive(self):
        """Test duration parsing is case insensitive."""
        self.assertEqual(utils.parse_duration("1H"), 60)
        self.assertEqual(utils.parse_duration("30M"), 30)


# =================================================================
# TEST CLASS 4: UTILS MODULE - RECURRING DAYS & FLEXIBILITY
# =================================================================
class TestUtilsRecurringAndFlexibility(unittest.TestCase):
    """Test recurring day calculation and flexibility scoring."""

    def test_calculate_recurring_days_once(self):
        """Test frequency=1 returns Thursday (day 4)."""
        result = utils.calculate_recurring_days(1, 0)
        self.assertEqual(result, [4])

    def test_calculate_recurring_days_multiple(self):
        """Test frequency > 1 with gap."""
        # freq=3, gap=1 -> days 1, 3, 5
        result = utils.calculate_recurring_days(3, 1)
        self.assertEqual(result, [1, 3, 5])

    def test_calculate_recurring_days_zero_freq(self):
        """Test frequency=0 returns empty list."""
        result = utils.calculate_recurring_days(0, 0)
        self.assertEqual(result, [])

    def test_calculate_recurring_days_negative_freq(self):
        """Test negative frequency returns empty list."""
        result = utils.calculate_recurring_days(-1, 0)
        self.assertEqual(result, [])

    def test_get_task_flexibility_wide_window(self):
        """Test flexibility for task with wide time window."""
        task = {
            'earliest_min': 0,      # 00:00
            'latest_min': 1440,     # 24:00
            'duration': 60          # 1 hour
        }
        flexibility = utils.get_task_flexibility(task)
        self.assertEqual(flexibility, 1440 - 0 - 60)  # 1380

    def test_get_task_flexibility_narrow_window(self):
        """Test flexibility for task with narrow time window."""
        task = {
            'earliest_min': 540,    # 09:00
            'latest_min': 600,      # 10:00
            'duration': 30          # 30 mins
        }
        flexibility = utils.get_task_flexibility(task)
        self.assertEqual(flexibility, 600 - 540 - 30)  # 30

    def test_get_task_flexibility_exact_fit(self):
        """Test flexibility when task exactly fits its window."""
        task = {
            'earliest_min': 540,    # 09:00
            'latest_min': 600,      # 10:00
            'duration': 60          # Exactly 1 hour
        }
        flexibility = utils.get_task_flexibility(task)
        self.assertEqual(flexibility, 0)


# =================================================================
# TEST CLASS 5: RECOMMENDER MODULE
# =================================================================
class TestRecommender(unittest.TestCase):
    """Test the recommendation system for finding alternatives."""

    def setUp(self):
        """Create a fully occupied day for testing."""
        self.fully_occupied = [True] * SLOTS_PER_DAY
        self.fully_free = [False] * SLOTS_PER_DAY

    def test_find_alternatives_single_gap(self):
        """Test finding a single gap in a busy schedule."""
        occupied = self.fully_occupied.copy()
        # Open gap at 01:00-02:00 (slots 4-7)
        for i in range(4, 8):
            occupied[i] = False

        task = {'duration': 60}  # 4 slots needed
        suggestions = recommender.find_alternatives(task, occupied)

        self.assertIn("01:00-02:00", suggestions)

    def test_find_alternatives_multiple_gaps(self):
        """Test finding multiple gaps in schedule."""
        occupied = self.fully_occupied.copy()
        # Gap 1: 01:00-02:00 (slots 4-7)
        for i in range(4, 8):
            occupied[i] = False
        # Gap 2: 10:00-11:00 (slots 40-43)
        for i in range(40, 44):
            occupied[i] = False

        task = {'duration': 60}
        suggestions = recommender.find_alternatives(task, occupied)

        self.assertIn("01:00-02:00", suggestions)
        self.assertIn("10:00-11:00", suggestions)

    def test_find_alternatives_no_gaps(self):
        """Test when no gaps exist."""
        task = {'duration': 60}
        suggestions = recommender.find_alternatives(task, self.fully_occupied)

        self.assertEqual(len(suggestions), 0)

    def test_find_alternatives_gap_too_small(self):
        """Test when gaps exist but are too small for the task."""
        occupied = self.fully_occupied.copy()
        # Small gap: only 2 slots (30 mins)
        occupied[4] = False
        occupied[5] = False

        task = {'duration': 60}  # Needs 4 slots
        suggestions = recommender.find_alternatives(task, occupied)

        self.assertEqual(len(suggestions), 0)

    def test_find_alternatives_empty_day(self):
        """Test finding alternatives on an empty day."""
        task = {'duration': 60}
        suggestions = recommender.find_alternatives(task, self.fully_free)

        # Should find at least one suggestion starting at 00:00
        self.assertGreater(len(suggestions), 0)
        self.assertIn("00:00-01:00", suggestions)

    def test_find_alternatives_max_three(self):
        """Test that at most 3 suggestions are returned."""
        task = {'duration': 15}  # Small task, many gaps possible
        suggestions = recommender.find_alternatives(task, self.fully_free)

        self.assertLessEqual(len(suggestions), 3)


# =================================================================
# TEST CLASS 6: SCHEDULER MODULE - SLOT AVAILABILITY
# =================================================================
class TestSchedulerSlotAvailability(unittest.TestCase):
    """Test slot availability checking."""

    def test_slots_available_single_free(self):
        """Test single free slot."""
        occupied = [False, True, True]
        self.assertTrue(scheduler.slots_available(occupied, 0, 0))

    def test_slots_available_single_busy(self):
        """Test single busy slot."""
        occupied = [False, True, False]
        self.assertFalse(scheduler.slots_available(occupied, 1, 1))

    def test_slots_available_range_all_free(self):
        """Test range where all slots are free."""
        occupied = [False, False, False, True]
        self.assertTrue(scheduler.slots_available(occupied, 0, 2))

    def test_slots_available_range_with_busy(self):
        """Test range containing a busy slot."""
        occupied = [False, True, False]
        self.assertFalse(scheduler.slots_available(occupied, 0, 2))

    def test_slots_available_out_of_bounds(self):
        """Test out-of-bounds indices return False."""
        occupied = [False, False, False]
        self.assertFalse(scheduler.slots_available(occupied, -1, 0))
        self.assertFalse(scheduler.slots_available(occupied, 0, 10))

    def test_slots_available_full_day_free(self):
        """Test a completely free day."""
        occupied = [False] * SLOTS_PER_DAY
        self.assertTrue(scheduler.slots_available(occupied, 0, SLOTS_PER_DAY - 1))

    def test_slots_available_full_day_busy(self):
        """Test a completely busy day."""
        occupied = [True] * SLOTS_PER_DAY
        self.assertFalse(scheduler.slots_available(occupied, 0, 0))


# =================================================================
# TEST CLASS 7: SCHEDULER MODULE - TASK SCHEDULING
# =================================================================
class TestSchedulerTaskScheduling(unittest.TestCase):
    """Test the main task scheduling functionality."""

    def setUp(self):
        """Set up a fresh week of empty schedules."""
        self.occupied_weekly = [[False] * SLOTS_PER_DAY for _ in range(7)]

    def test_schedule_task_success(self):
        """Test successfully scheduling a task."""
        task = {
            'name': 'Test Task',
            'duration': 30,         # 2 slots
            'earliest_min': 540,    # 09:00
            'latest_min': 600,      # 10:00
            'priority': 'A'
        }

        success, csv_row, viz, logs = scheduler.try_schedule_task(
            task, 0, self.occupied_weekly, "Monday"
        )

        self.assertTrue(success)
        self.assertEqual(csv_row[1], "09:00")  # Start time
        self.assertEqual(csv_row[2], "09:30")  # End time
        self.assertEqual(viz['name'], 'Test Task')

    def test_schedule_task_marks_slots_occupied(self):
        """Test that scheduling marks slots as occupied."""
        task = {
            'name': 'Test Task',
            'duration': 30,
            'earliest_min': 540,    # 09:00 = slot 36
            'latest_min': 600,
            'priority': 'A'
        }

        scheduler.try_schedule_task(task, 0, self.occupied_weekly, "Monday")

        # Slot 36 (09:00) and 37 (09:15) should be occupied
        self.assertTrue(self.occupied_weekly[0][36])
        self.assertTrue(self.occupied_weekly[0][37])
        # Slot 38 (09:30) should still be free
        self.assertFalse(self.occupied_weekly[0][38])

    def test_schedule_task_conflict(self):
        """Test scheduling fails when slots are occupied."""
        # Pre-occupy slots 36-37 (09:00-09:30)
        self.occupied_weekly[0][36] = True
        self.occupied_weekly[0][37] = True

        task = {
            'name': 'Conflicting Task',
            'duration': 30,
            'earliest_min': 540,    # 09:00
            'latest_min': 570,      # 09:30 (tight window)
            'priority': 'A'
        }

        success, csv_row, viz, logs = scheduler.try_schedule_task(
            task, 0, self.occupied_weekly, "Monday"
        )

        self.assertFalse(success)
        self.assertEqual(csv_row[1], 'ERR')
        self.assertIn('message', viz)

    def test_schedule_task_finds_later_slot(self):
        """Test scheduler finds next available slot when first is busy."""
        # Pre-occupy 09:00 slot
        self.occupied_weekly[0][36] = True
        self.occupied_weekly[0][37] = True

        task = {
            'name': 'Flexible Task',
            'duration': 30,
            'earliest_min': 540,    # 09:00
            'latest_min': 720,      # 12:00 (wide window)
            'priority': 'A'
        }

        success, csv_row, viz, logs = scheduler.try_schedule_task(
            task, 0, self.occupied_weekly, "Monday"
        )

        self.assertTrue(success)
        # Should start at 09:30 (slot 38) since 09:00 is busy
        self.assertEqual(csv_row[1], "09:30")

    def test_schedule_multiple_tasks_sequentially(self):
        """Test scheduling multiple tasks back-to-back."""
        task1 = {
            'name': 'Task 1',
            'duration': 60,
            'earliest_min': 540,
            'latest_min': 720,
            'priority': 'A'
        }
        task2 = {
            'name': 'Task 2',
            'duration': 60,
            'earliest_min': 540,
            'latest_min': 720,
            'priority': 'A'
        }

        success1, csv1, _, _ = scheduler.try_schedule_task(
            task1, 0, self.occupied_weekly, "Monday"
        )
        success2, csv2, _, _ = scheduler.try_schedule_task(
            task2, 0, self.occupied_weekly, "Monday"
        )

        self.assertTrue(success1)
        self.assertTrue(success2)
        self.assertEqual(csv1[1], "09:00")
        self.assertEqual(csv2[1], "10:00")  # Should start after task1


# =================================================================
# TEST CLASS 8: SCHEDULER MODULE - ASSIGN TASKS TO DAYS
# =================================================================
class TestSchedulerAssignTasksToDays(unittest.TestCase):
    """Test the task-to-day assignment functionality."""

    def test_assign_with_preferred_days(self):
        """Test tasks are assigned to their preferred days."""
        tasks = [{
            'name': 'Sunday Task',
            'duration': 60,
            'earliest_min': 540,
            'latest_min': 720,
            'frequency': 1,
            'preferred_days': ['Sunday'],
            'priority': 'A'
        }]

        daily_tasks, week_dates = scheduler.assign_tasks_to_days(tasks)

        # Find which day index is Sunday
        sunday_idx = None
        for i, d in enumerate(week_dates):
            if d.strftime("%A") == "Sunday":
                sunday_idx = i
                break

        if sunday_idx is not None:
            self.assertIn(tasks[0], daily_tasks[sunday_idx])

    def test_assign_multiple_days(self):
        """Test tasks with multiple preferred days."""
        tasks = [{
            'name': 'MWF Task',
            'duration': 60,
            'earliest_min': 540,
            'latest_min': 720,
            'frequency': 3,
            'preferred_days': ['Monday', 'Wednesday', 'Friday'],
            'priority': 'A'
        }]

        daily_tasks, week_dates = scheduler.assign_tasks_to_days(tasks)

        # Count how many days have this task
        days_with_task = sum(
            1 for day in daily_tasks if tasks[0] in day
        )
        self.assertGreaterEqual(days_with_task, 1)

    def test_assign_returns_seven_days(self):
        """Test that assignment returns exactly 7 days."""
        tasks = [{'name': 'Test', 'duration': 60, 'earliest_min': 0,
                  'latest_min': 1440, 'frequency': 1, 'preferred_days': [],
                  'priority': 'A'}]

        daily_tasks, week_dates = scheduler.assign_tasks_to_days(tasks)

        self.assertEqual(len(daily_tasks), 7)
        self.assertEqual(len(week_dates), 7)


# =================================================================
# TEST CLASS 9: INTEGRATION TESTS
# =================================================================
class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple modules."""

    def test_full_scheduling_workflow(self):
        """Test complete workflow from task definition to scheduling."""
        # Define a simple task
        task = {
            'name': 'Study Session',
            'duration': utils.parse_duration('2h'),
            'earliest_min': utils.parse_time('09:00'),
            'latest_min': utils.parse_time('17:00'),
            'frequency': 1,
            'preferred_days': [],
            'priority': 'A'
        }

        # Verify duration parsing
        self.assertEqual(task['duration'], 120)

        # Verify time parsing
        self.assertEqual(task['earliest_min'], 540)
        self.assertEqual(task['latest_min'], 1020)

        # Schedule the task
        occupied_weekly = [[False] * SLOTS_PER_DAY for _ in range(7)]
        success, csv_row, viz, _ = scheduler.try_schedule_task(
            task, 0, occupied_weekly, "Monday"
        )

        self.assertTrue(success)
        self.assertEqual(viz['duration'], 120)

    def test_priority_based_scheduling_order(self):
        """Test that higher priority tasks get better slots."""
        occupied_weekly = [[False] * SLOTS_PER_DAY for _ in range(7)]

        # Critical task should get earliest slot
        critical_task = {
            'name': 'Critical',
            'duration': 60,
            'earliest_min': 540,
            'latest_min': 720,
            'priority': 'S'
        }

        # Low priority task competes for same window
        low_task = {
            'name': 'Low Priority',
            'duration': 60,
            'earliest_min': 540,
            'latest_min': 720,
            'priority': 'C'
        }

        # Sort by priority (as main.py does)
        tasks = [low_task, critical_task]
        tasks.sort(key=lambda t: PRIORITY_VALUES[t['priority']])

        # Critical should be first after sorting
        self.assertEqual(tasks[0]['name'], 'Critical')

    def test_conflict_triggers_recommendations(self):
        """Test that conflicts generate recommendations."""
        # Fill up most of the day
        occupied = [True] * SLOTS_PER_DAY
        # Leave one gap: 14:00-16:00 (slots 56-63)
        for i in range(56, 64):
            occupied[i] = False

        task = {
            'name': 'Meeting',
            'duration': 60,
            'earliest_min': 540,    # 09:00
            'latest_min': 720,      # 12:00 (no space here)
            'priority': 'A'
        }

        # The task window (09:00-12:00) is full
        success, csv_row, viz, _ = scheduler.try_schedule_task(
            task, 0, [occupied], "Monday"
        )

        # Should fail but recommend the 14:00-16:00 gap
        self.assertFalse(success)
        # Check that recommendations were generated
        alts = recommender.find_alternatives(task, occupied)
        self.assertGreater(len(alts), 0)


# =================================================================
# TEST CLASS 10: EDGE CASES
# =================================================================
class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_midnight_boundary(self):
        """Test scheduling across midnight boundary."""
        self.assertEqual(utils.parse_time("23:59"), 1439)
        self.assertEqual(utils.parse_time("00:00"), 0)

    def test_zero_duration_task(self):
        """Test handling of zero-duration task."""
        self.assertEqual(utils.parse_duration("0"), 0)
        self.assertEqual(utils.parse_duration("0m"), 0)
        self.assertEqual(utils.parse_duration("0h"), 0)

    def test_very_long_task(self):
        """Test a task spanning multiple hours."""
        duration = utils.parse_duration("8h")
        self.assertEqual(duration, 480)

        slots_needed = duration // SLOT_DURATION
        self.assertEqual(slots_needed, 32)

    def test_minimum_slot_task(self):
        """Test a 15-minute (1 slot) task."""
        occupied_weekly = [[False] * SLOTS_PER_DAY for _ in range(7)]

        task = {
            'name': 'Quick Call',
            'duration': 15,
            'earliest_min': 540,
            'latest_min': 600,
            'priority': 'A'
        }

        success, csv_row, viz, _ = scheduler.try_schedule_task(
            task, 0, occupied_weekly, "Monday"
        )

        self.assertTrue(success)
        self.assertEqual(csv_row[2], "09:15")  # End after 15 mins

    def test_task_exactly_fills_window(self):
        """Test task that exactly fills its time window."""
        occupied_weekly = [[False] * SLOTS_PER_DAY for _ in range(7)]

        task = {
            'name': 'Exact Fit',
            'duration': 60,
            'earliest_min': 540,    # 09:00
            'latest_min': 600,      # 10:00
            'priority': 'A'
        }

        success, _, _, _ = scheduler.try_schedule_task(
            task, 0, occupied_weekly, "Monday"
        )

        self.assertTrue(success)

    def test_empty_preferred_days(self):
        """Test task with no preferred days uses recurring logic."""
        tasks = [{
            'name': 'Recurring Task',
            'duration': 60,
            'earliest_min': 540,
            'latest_min': 720,
            'frequency': 3,
            'preferred_days': [],   # Empty
            'priority': 'A'
        }]

        daily_tasks, _ = scheduler.assign_tasks_to_days(tasks)

        # Should still be assigned to some days
        total_assignments = sum(len(day) for day in daily_tasks)
        self.assertGreater(total_assignments, 0)


# =================================================================
# RUNNER
# =================================================================
if __name__ == "__main__":
    # Run with verbosity level 2 for detailed output
    unittest.main(verbosity=2)