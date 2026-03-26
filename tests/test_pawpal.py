import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path so we can import pawpal_system
sys.path.insert(0, str(Path(__file__).parent.parent))

from pawpal_system import Task, Pet, Owner, Schedule


class TestTask:
    """Tests for Task class."""
    
    def test_task_completion(self):
        """Verify that calling mark_complete() changes the task's completion status."""
        # Create a task with completion_status = False by default
        task = Task(
            title="Morning Walk",
            description="Take dog for a walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        # Verify initial status is False
        assert task.completion_status is False, "Task should start incomplete"
        
        # Mark task as complete
        task.mark_complete()
        
        # Verify status changed to True
        assert task.completion_status is True, "Task should be marked complete after calling mark_complete()"


class TestPet:
    """Tests for Pet class."""
    
    def test_task_addition(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Create a pet
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=["energetic"],
            care_requirements={"min_walks_per_day": 2}
        )
        
        # Verify pet starts with 0 tasks
        initial_task_count = len(pet.get_required_tasks())
        assert initial_task_count == 0, "Pet should start with no tasks"
        
        # Create and add first task
        task1 = Task(
            title="Morning Walk",
            description="30-min walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        pet.add_task(task1)
        
        # Verify task count increased to 1
        assert len(pet.get_required_tasks()) == 1, "Pet should have 1 task after adding one"
        
        # Create and add second task
        task2 = Task(
            title="Feeding",
            description="Feed breakfast",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily"
        )
        pet.add_task(task2)
        
        # Verify task count increased to 2
        assert len(pet.get_required_tasks()) == 2, "Pet should have 2 tasks after adding two"
        
        # Verify the returned tasks are the ones we added
        tasks = pet.get_required_tasks()
        assert tasks[0].title == "Morning Walk"
        assert tasks[1].title == "Feeding"


class TestOwner:
    """Tests for Owner class."""
    
    def test_filter_tasks_by_pet_name(self):
        """Verify that filter_tasks() correctly filters tasks by pet name."""
        # Create owner
        owner = Owner(
            name="Harshal",
            available_hours_per_day=4.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        # Create two pets
        mochi = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=[],
            care_requirements={}
        )
        
        whiskers = Pet(
            name="Whiskers",
            species="cat",
            age=5,
            special_needs=[],
            care_requirements={}
        )
        
        owner.add_pet(mochi)
        owner.add_pet(whiskers)
        
        # Add tasks to Mochi
        task_mochi_walk = Task(
            title="Mochi Walk",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily"
        )
        mochi.add_task(task_mochi_walk)
        
        # Add tasks to Whiskers
        task_whiskers_feed = Task(
            title="Whiskers Food",
            description="Feed",
            duration_minutes=10,
            priority="high",
            task_type="feed",
            frequency="daily"
        )
        whiskers.add_task(task_whiskers_feed)
        
        # Filter by Mochi
        mochi_tasks = owner.filter_tasks(pet_name="Mochi")
        assert len(mochi_tasks) == 1, "Should have 1 task for Mochi"
        assert mochi_tasks[0].title == "Mochi Walk"
        
        # Filter by Whiskers
        whiskers_tasks = owner.filter_tasks(pet_name="Whiskers")
        assert len(whiskers_tasks) == 1, "Should have 1 task for Whiskers"
        assert whiskers_tasks[0].title == "Whiskers Food"
        
        # No filter - should return all tasks
        all_tasks = owner.filter_tasks()
        assert len(all_tasks) == 2, "Should have 2 total tasks"
    
    def test_filter_tasks_by_completion_status(self):
        """Verify that filter_tasks() correctly filters by completion status."""
        # Create owner and pet
        owner = Owner(
            name="Harshal",
            available_hours_per_day=4.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=[],
            care_requirements={}
        )
        
        owner.add_pet(pet)
        
        # Create and add tasks
        task1 = Task(
            title="Walk",
            description="Morning walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily"
        )
        
        task2 = Task(
            title="Feed",
            description="Breakfast",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily"
        )
        
        task3 = Task(
            title="Playtime",
            description="Play session",
            duration_minutes=20,
            priority="low",
            task_type="enrichment",
            frequency="daily"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Mark some tasks as complete
        task1.mark_complete()
        task2.mark_complete()
        
        # Filter incomplete tasks
        incomplete_tasks = owner.filter_tasks(completion_status=False)
        assert len(incomplete_tasks) == 1, "Should have 1 incomplete task"
        assert incomplete_tasks[0].title == "Playtime"
        
        # Filter completed tasks
        completed_tasks = owner.filter_tasks(completion_status=True)
        assert len(completed_tasks) == 2, "Should have 2 completed tasks"
        assert completed_tasks[0].title == "Walk"
        assert completed_tasks[1].title == "Feed"
    
    def test_filter_tasks_by_pet_and_status(self):
        """Verify that filter_tasks() works with both pet name and completion status."""
        # Create owner
        owner = Owner(
            name="Harshal",
            available_hours_per_day=4.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        # Create two pets
        mochi = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=[],
            care_requirements={}
        )
        
        whiskers = Pet(
            name="Whiskers",
            species="cat",
            age=5,
            special_needs=[],
            care_requirements={}
        )
        
        owner.add_pet(mochi)
        owner.add_pet(whiskers)
        
        # Add and mark tasks for Mochi
        mochi_task1 = Task(
            title="Mochi Walk",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily"
        )
        mochi_task2 = Task(
            title="Mochi Feed",
            description="Feed",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily"
        )
        mochi.add_task(mochi_task1)
        mochi.add_task(mochi_task2)
        mochi_task1.mark_complete()
        
        # Add and mark tasks for Whiskers
        whiskers_task1 = Task(
            title="Whiskers Food",
            description="Feed",
            duration_minutes=10,
            priority="high",
            task_type="feed",
            frequency="daily"
        )
        whiskers.add_task(whiskers_task1)
        whiskers_task1.mark_complete()
        
        # Filter: incomplete tasks for Mochi only
        mochi_incomplete = owner.filter_tasks(pet_name="Mochi", completion_status=False)
        assert len(mochi_incomplete) == 1, "Should have 1 incomplete task for Mochi"
        assert mochi_incomplete[0].title == "Mochi Feed"
        
        # Filter: completed tasks for Mochi only
        mochi_complete = owner.filter_tasks(pet_name="Mochi", completion_status=True)
        assert len(mochi_complete) == 1, "Should have 1 completed task for Mochi"
        assert mochi_complete[0].title == "Mochi Walk"


class TestSchedule:
    """Tests for Schedule class."""
    
    def test_sort_by_time(self):
        """Verify that sort_by_time() correctly sorts tasks by their required_time attribute."""
        # Create owner and pet
        owner = Owner(
            name="Harshal",
            available_hours_per_day=4.0,
            preferred_activity_times=["morning", "evening"],
            preferences={}
        )
        
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=[],
            care_requirements={}
        )
        
        owner.add_pet(pet)
        
        # Create a schedule
        schedule = Schedule(owner=owner, pet=pet)
        
        # Create tasks with different times (intentionally out of order)
        task_evening = Task(
            title="Evening Walk",
            description="Walk at 6pm",
            duration_minutes=30,
            priority="medium",
            task_type="walk",
            frequency="daily",
            required_time="6:00pm"
        )
        
        task_morning = Task(
            title="Morning Walk",
            description="Walk at 7am",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        task_noon = Task(
            title="Noon Feeding",
            description="Feed at 12pm",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            required_time="12:00pm"
        )
        
        task_no_time = Task(
            title="Playtime",
            description="Play when available",
            duration_minutes=20,
            priority="low",
            task_type="enrichment",
            frequency="daily"
        )
        
        # Add tasks in random order
        schedule.add_task(task_evening)
        schedule.add_task(task_morning)
        schedule.add_task(task_no_time)
        schedule.add_task(task_noon)
        
        # Sort by time
        sorted_tasks = schedule.sort_by_time()
        
        # Verify correct order: 7:00am, 12:00pm, 6:00pm, then tasks without time
        assert sorted_tasks[0].title == "Morning Walk", "First task should be Morning Walk (7:00am)"
        assert sorted_tasks[1].title == "Noon Feeding", "Second task should be Noon Feeding (12:00pm)"
        assert sorted_tasks[2].title == "Evening Walk", "Third task should be Evening Walk (6:00pm)"
        assert sorted_tasks[3].title == "Playtime", "Last task should be Playtime (no required time)"
    
    def test_recurring_daily_task_creation(self):
        """Verify that marking a daily recurring task complete creates a new instance for the next day."""
        # Create pet
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=[],
            care_requirements={}
        )
        
        # Create a daily recurring task with a specific date
        test_date = datetime(2026, 3, 25, 14, 30, 0)  # Fixed date for testing
        daily_task = Task(
            title="Daily Walk",
            description="Morning walk around the park",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am",
            task_date=test_date
        )
        
        pet.add_task(daily_task)
        
        # Verify initial state: 1 task, not complete
        assert len(pet.get_required_tasks()) == 1, "Should have 1 task initially"
        assert daily_task.completion_status is False, "Task should be incomplete"
        
        # Mark task as complete
        result = pet.mark_task_complete("Daily Walk")
        
        # Verify: original task is marked complete AND new task created for tomorrow
        assert result is True, "mark_task_complete() should return True"
        assert daily_task.completion_status is True, "Original task should be marked complete"
        assert len(pet.get_required_tasks()) == 2, "Should have 2 tasks after completing recurring task"
        
        # Verify new task has next day's date using timedelta
        new_task = pet.get_required_tasks()[1]
        expected_next_date = test_date.date() + timedelta(days=1)
        actual_next_date = new_task.task_date.date() if new_task.task_date else None
        
        assert new_task.title == "Daily Walk", "New task should have same title"
        assert new_task.completion_status is False, "New task should be incomplete"
        assert actual_next_date == expected_next_date, f"New task date should be {expected_next_date}, got {actual_next_date}"
    
    def test_recurring_weekly_task_creation(self):
        """Verify that marking a weekly recurring task complete creates a new instance for next week."""
        # Create pet
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=[],
            care_requirements={}
        )
        
        # Create a weekly recurring task with a specific date for testing
        test_date = datetime(2026, 3, 25, 10, 0, 0)  # Wednesday
        weekly_task = Task(
            title="Grooming Session",
            description="Weekly bath and grooming",
            duration_minutes=60,
            priority="medium",
            task_type="grooming",
            frequency="weekly",
            task_date=test_date
        )
        
        pet.add_task(weekly_task)
        
        # Mark task as complete
        result = pet.mark_task_complete("Grooming Session")
        
        # Verify: original task is marked complete AND new task created for next week
        assert result is True, "mark_task_complete() should return True"
        assert weekly_task.completion_status is True, "Original task should be marked complete"
        assert len(pet.get_required_tasks()) == 2, "Should have 2 tasks after completing recurring task"
        
        # Verify new task has next week's date using timedelta (7 days)
        new_task = pet.get_required_tasks()[1]
        expected_next_date = test_date.date() + timedelta(days=7)
        actual_next_date = new_task.task_date.date() if new_task.task_date else None
        
        assert new_task.title == "Grooming Session", "New task should have same title"
        assert new_task.completion_status is False, "New task should be incomplete"
        assert actual_next_date == expected_next_date, f"New task date should be {expected_next_date}, got {actual_next_date}"
    
    def test_non_recurring_task_does_not_create_new_instance(self):
        """Verify that marking a 'once' task complete does NOT create a new instance."""
        # Create pet
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=[],
            care_requirements={}
        )
        
        # Create a one-time task
        one_time_task = Task(
            title="Vet Appointment",
            description="Annual checkup",
            duration_minutes=45,
            priority="high",
            task_type="medical",
            frequency="once"
        )
        
        pet.add_task(one_time_task)
        
        # Verify initial state
        assert len(pet.get_required_tasks()) == 1, "Should have 1 task initially"
        
        # Mark task as complete
        result = pet.mark_task_complete("Vet Appointment")
        
        # Verify: task marked complete but NO new task created
        assert result is True, "mark_task_complete() should return True"
        assert one_time_task.completion_status is True, "Task should be marked complete"
        assert len(pet.get_required_tasks()) == 1, "Should still have only 1 task (no new instance)"
    
    def test_mark_nonexistent_task_returns_false(self):
        """Verify that marking a non-existent task returns False."""
        # Create pet
        pet = Pet(
            name="Mochi",
            species="dog",
            age=3,
            special_needs=[],
            care_requirements={}
        )
        
        # Add a task
        task = Task(
            title="Walk",
            description="Morning walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily"
        )
        pet.add_task(task)
        
        # Try to mark a non-existent task
        result = pet.mark_task_complete("Non-existent Task")
        
        # Verify: returns False and no new task was created
        assert result is False, "mark_task_complete() should return False for non-existent task"
        assert len(pet.get_required_tasks()) == 1, "Should still have only 1 task"


class TestConflictDetection:
    """Tests for conflict detection in scheduling."""
    
    def test_no_conflicts_separate_times(self):
        """Verify that tasks at different times have no conflicts."""
        owner = Owner(
            name="Harshal",
            available_hours_per_day=8.0,
            preferred_activity_times=["morning", "evening"],
            preferences={}
        )
        
        pet = Pet(name="Mochi", species="dog", age=3, special_needs=[], care_requirements={})
        owner.add_pet(pet)
        
        task1 = Task(
            title="Morning Walk",
            description="7am walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        task2 = Task(
            title="Afternoon Walk",
            description="3pm walk",
            duration_minutes=30,
            priority="medium",
            task_type="walk",
            frequency="daily",
            required_time="3:00pm"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet)
        schedule.add_task(task1)
        schedule.add_task(task2)
        schedule.daily_plan = [(task1, "7:00am"), (task2, "3:00pm")]
        
        conflicts = schedule.detect_conflicts()
        
        assert len(conflicts["hard"]) == 0, "Should have no hard conflicts"
        assert len(conflicts["soft"]) == 0, "Should have no soft conflicts"
    
    def test_hard_conflict_overlapping_tasks(self):
        """Verify that overlapping tasks are detected as hard conflicts."""
        owner = Owner(
            name="Harshal",
            available_hours_per_day=8.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        pet = Pet(name="Mochi", species="dog", age=3, special_needs=[], care_requirements={})
        owner.add_pet(pet)
        
        # Create two overlapping tasks
        task1 = Task(
            title="Walk 1",
            description="First walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        task2 = Task(
            title="Walk 2",
            description="Second walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:15am"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet)
        schedule.add_task(task1)
        schedule.add_task(task2)
        schedule.daily_plan = [(task1, "7:00am"), (task2, "7:15am")]
        
        conflicts = schedule.detect_conflicts()
        
        assert len(conflicts["hard"]) > 0, "Should have at least one hard conflict"
        assert "OVERLAP" in conflicts["hard"][0], "Conflict should mention overlap"
    
    def test_soft_conflict_tight_gap(self):
        """Verify that tasks with tight gaps (< buffer) are detected as soft conflicts."""
        owner = Owner(
            name="Harshal",
            available_hours_per_day=8.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        pet = Pet(name="Mochi", species="dog", age=3, special_needs=[], care_requirements={})
        owner.add_pet(pet)
        
        # Create two tasks with only 3 minute gap (default buffer is 5)
        task1 = Task(
            title="Walk",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        task2 = Task(
            title="Feeding",
            description="Feeding",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            required_time="7:33am"  # Only 3 minute gap after 7:00am + 30min
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet)
        schedule.add_task(task1)
        schedule.add_task(task2)
        schedule.daily_plan = [(task1, "7:00am"), (task2, "7:33am")]
        
        conflicts = schedule.detect_conflicts(buffer_minutes=5)
        
        assert len(conflicts["soft"]) > 0, "Should have at least one soft conflict"
        assert "TIGHT" in conflicts["soft"][0], "Conflict should mention tight gap"
    
    def test_cross_pet_hard_conflict(self):
        """Verify that overlapping tasks for different pets are detected as cross-pet conflicts."""
        owner = Owner(
            name="Harshal",
            available_hours_per_day=8.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        pet1 = Pet(name="Mochi", species="dog", age=3, special_needs=[], care_requirements={})
        pet2 = Pet(name="Whiskers", species="cat", age=5, special_needs=[], care_requirements={})
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        # Task for Mochi
        task1 = Task(
            title="Mochi Walk",
            description="Dog walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        # Task for Whiskers at same time
        task2 = Task(
            title="Whiskers Feed",
            description="Cat feeding",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            required_time="7:00am"  # Same time as Mochi's walk
        )
        
        pet1.add_task(task1)
        pet2.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet1)
        schedule.add_task(task1)
        schedule.add_task(task2)
        schedule.daily_plan = [(task1, "7:00am"), (task2, "7:00am")]
        
        conflicts = schedule.detect_conflicts()
        
        assert len(conflicts["hard"]) > 0, "Should detect conflict between different pets at same time"


class TestSortingCorrectness:
    """Comprehensive tests for task sorting and chronological ordering."""
    
    def test_sort_by_time_chronological_order(self):
        """Verify tasks are returned in strict chronological order."""
        owner = Owner(name="Test", available_hours_per_day=8.0)
        pet = Pet(name="TestPet", species="dog", age=3)
        schedule = Schedule(owner=owner, pet=pet)
        
        # Create tasks spanning entire day
        times = ["6:30am", "9:15am", "12:00pm", "3:45pm", "8:00pm", "11:59pm"]
        for i, time in enumerate(times):
            task = Task(
                title=f"Task {i}",
                description=f"Task at {time}",
                duration_minutes=15,
                priority="medium",
                task_type="activity",
                frequency="daily",
                required_time=time
            )
            schedule.add_task(task)
        
        sorted_tasks = schedule.sort_by_time()
        
        # Verify order is maintained
        for i in range(len(sorted_tasks) - 1):
            current_time = sorted_tasks[i].required_time
            next_time = sorted_tasks[i + 1].required_time
            current_minutes = time_to_minutes(current_time)
            next_minutes = time_to_minutes(next_time)
            assert current_minutes <= next_minutes, \
                f"Sort order violated: {current_time} should come before {next_time}"
    
    def test_sort_by_time_with_empty_list(self):
        """Verify sorting empty task list returns empty list."""
        owner = Owner(name="Test", available_hours_per_day=8.0)
        pet = Pet(name="TestPet", species="dog", age=3)
        schedule = Schedule(owner=owner, pet=pet)
        
        sorted_tasks = schedule.sort_by_time()
        
        assert sorted_tasks == [], "Sorting empty list should return empty list"
    
    def test_sort_by_time_all_same_time(self):
        """Verify sorting tasks with identical times maintains all tasks."""
        owner = Owner(name="Test", available_hours_per_day=8.0)
        pet = Pet(name="TestPet", species="dog", age=3)
        schedule = Schedule(owner=owner, pet=pet)
        
        # All tasks at 9:00am
        for i in range(3):
            task = Task(
                title=f"Task {i}",
                description="All at same time",
                duration_minutes=15,
                priority="medium",
                task_type="activity",
                frequency="daily",
                required_time="9:00am"
            )
            schedule.add_task(task)
        
        sorted_tasks = schedule.sort_by_time()
        
        assert len(sorted_tasks) == 3, "Should have all 3 tasks"
        for task in sorted_tasks:
            assert task.required_time == "9:00am", "All tasks should maintain 9:00am time"
    
    def test_sort_by_time_midnight_boundary(self):
        """Verify correct sorting at midnight boundaries (12am to 1am)."""
        owner = Owner(name="Test", available_hours_per_day=8.0)
        pet = Pet(name="TestPet", species="dog", age=3)
        schedule = Schedule(owner=owner, pet=pet)
        
        task_midnight = Task(
            title="Midnight Task",
            description="At midnight",
            duration_minutes=15,
            priority="high",
            task_type="activity",
            frequency="daily",
            required_time="12:00am"
        )
        
        task_early_morning = Task(
            title="Early Morning",
            description="Just after midnight",
            duration_minutes=15,
            priority="high",
            task_type="activity",
            frequency="daily",
            required_time="12:30am"
        )
        
        task_late_night = Task(
            title="Late Night",
            description="Before midnight",
            duration_minutes=15,
            priority="high",
            task_type="activity",
            frequency="daily",
            required_time="11:59pm"
        )
        
        schedule.add_task(task_late_night)
        schedule.add_task(task_midnight)
        schedule.add_task(task_early_morning)
        
        sorted_tasks = schedule.sort_by_time()
        
        # Verify order: 12am, 12:30am, then 11:59pm (wraps)
        assert sorted_tasks[0].title == "Midnight Task"
        assert sorted_tasks[1].title == "Early Morning"
        assert sorted_tasks[2].title == "Late Night"
    
    def test_sort_priority_vs_time_without_required_time(self):
        """Verify tasks without required_time are placed at end of sorted list."""
        owner = Owner(name="Test", available_hours_per_day=8.0)
        pet = Pet(name="TestPet", species="dog", age=3)
        schedule = Schedule(owner=owner, pet=pet)
        
        task_with_time = Task(
            title="Scheduled",
            description="Has time",
            duration_minutes=15,
            priority="low",
            task_type="activity",
            frequency="daily",
            required_time="2:00pm"
        )
        
        task_no_time_high = Task(
            title="Flexible High",
            description="No time, high priority",
            duration_minutes=15,
            priority="high",
            task_type="activity",
            frequency="daily"
        )
        
        task_no_time_low = Task(
            title="Flexible Low",
            description="No time, low priority",
            duration_minutes=15,
            priority="low",
            task_type="activity",
            frequency="daily"
        )
        
        schedule.add_task(task_no_time_low)
        schedule.add_task(task_with_time)
        schedule.add_task(task_no_time_high)
        
        sorted_tasks = schedule.sort_by_time()
        
        # First task should be the one with time
        assert sorted_tasks[0].title == "Scheduled"
        # Remaining two should be the ones without time
        assert sorted_tasks[1] in [task_no_time_high, task_no_time_low]
        assert sorted_tasks[2] in [task_no_time_high, task_no_time_low]


class TestRecurrenceLogic:
    """Comprehensive tests for recurring task creation and management."""
    
    def test_recurring_daily_without_task_date(self):
        """Verify daily recurring task works when task_date is None (uses today)."""
        pet = Pet(name="TestPet", species="dog", age=3)
        
        # Create daily task without explicit task_date
        daily_task = Task(
            title="Daily Feed",
            description="Feed daily",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily"
        )
        
        pet.add_task(daily_task)
        assert len(pet.get_required_tasks()) == 1
        
        # Mark complete - should create next instance
        result = pet.mark_task_complete("Daily Feed")
        
        assert result is True, "Should successfully mark task complete"
        assert len(pet.get_required_tasks()) == 2, "Should create new instance"
        assert pet.get_required_tasks()[0].completion_status is True, "Original should be complete"
        assert pet.get_required_tasks()[1].completion_status is False, "New should be incomplete"
    
    def test_recurring_daily_correct_date_increment(self):
        """Verify daily task increments by exactly 1 day."""
        pet = Pet(name="TestPet", species="dog", age=3)
        
        test_date = datetime(2026, 3, 15, 10, 30)
        daily_task = Task(
            title="Daily",
            description="",
            duration_minutes=15,
            priority="high",
            task_type="activity",
            frequency="daily",
            task_date=test_date
        )
        
        pet.add_task(daily_task)
        pet.mark_task_complete("Daily")
        
        new_task = pet.get_required_tasks()[1]
        expected_date = datetime(2026, 3, 16)
        actual_date = new_task.task_date.date() if new_task.task_date else None
        
        assert actual_date == expected_date.date(), \
            f"Expected {expected_date.date()}, got {actual_date}"
    
    def test_recurring_weekly_correct_date_increment(self):
        """Verify weekly task increments by exactly 7 days."""
        pet = Pet(name="TestPet", species="dog", age=3)
        
        test_date = datetime(2026, 3, 15, 10, 30)  # Sunday
        weekly_task = Task(
            title="Weekly",
            description="",
            duration_minutes=60,
            priority="medium",
            task_type="grooming",
            frequency="weekly",
            task_date=test_date
        )
        
        pet.add_task(weekly_task)
        pet.mark_task_complete("Weekly")
        
        new_task = pet.get_required_tasks()[1]
        expected_date = datetime(2026, 3, 22)  # Exactly 7 days later
        actual_date = new_task.task_date.date() if new_task.task_date else None
        
        assert actual_date == expected_date.date(), \
            f"Expected {expected_date.date()}, got {actual_date}"
    
    def test_multiple_recurring_tasks_independent(self):
        """Verify multiple recurring tasks track dates independently."""
        pet = Pet(name="TestPet", species="dog", age=3)
        
        daily_date = datetime(2026, 3, 15, 8, 0)
        weekly_date = datetime(2026, 3, 15, 10, 0)
        
        daily_task = Task(
            title="Daily",
            description="",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            task_date=daily_date
        )
        
        weekly_task = Task(
            title="Weekly",
            description="",
            duration_minutes=60,
            priority="medium",
            task_type="grooming",
            frequency="weekly",
            task_date=weekly_date
        )
        
        pet.add_task(daily_task)
        pet.add_task(weekly_task)
        
        pet.mark_task_complete("Daily")
        pet.mark_task_complete("Weekly")
        
        all_tasks = pet.get_required_tasks()
        assert len(all_tasks) == 4, "Should have 4 total tasks (2 original + 2 new)"
        
        # Find the new daily task
        new_daily = [t for t in all_tasks if t.title == "Daily" and not t.completion_status][0]
        # Find the new weekly task
        new_weekly = [t for t in all_tasks if t.title == "Weekly" and not t.completion_status][0]
        
        expected_daily_date = daily_date.date() + timedelta(days=1)
        expected_weekly_date = weekly_date.date() + timedelta(days=7)
        
        assert new_daily.task_date.date() == expected_daily_date
        assert new_weekly.task_date.date() == expected_weekly_date
    
    def test_recurring_task_properties_preserved(self):
        """Verify recurring task creates new instance with identical properties."""
        pet = Pet(name="TestPet", species="dog", age=3)
        
        original_task = Task(
            title="Preserve Props",
            description="Test description",
            duration_minutes=45,
            priority="high",
            task_type="medical",
            frequency="daily",
            required_time="8:30am",
            task_date=datetime(2026, 3, 15)
        )
        
        pet.add_task(original_task)
        pet.mark_task_complete("Preserve Props")
        
        new_task = pet.get_required_tasks()[1]
        
        assert new_task.title == original_task.title
        assert new_task.description == original_task.description
        assert new_task.duration_minutes == original_task.duration_minutes
        assert new_task.priority == original_task.priority
        assert new_task.task_type == original_task.task_type
        assert new_task.frequency == original_task.frequency
        assert new_task.required_time == original_task.required_time
    
    def test_chain_mark_multiple_daily_tasks(self):
        """Verify marking multiple daily tasks complete in sequence works correctly."""
        pet = Pet(name="TestPet", species="dog", age=3)
        
        base_date = datetime(2026, 3, 15, 10, 0)
        
        for i in range(3):
            task = Task(
                title=f"Task {i}",
                description="",
                duration_minutes=15,
                priority="high",
                task_type="activity",
                frequency="daily",
                task_date=base_date
            )
            pet.add_task(task)
        
        # Mark all three complete
        for i in range(3):
            pet.mark_task_complete(f"Task {i}")
        
        # Should have 6 tasks total (3 original + 3 new)
        assert len(pet.get_required_tasks()) == 6
        
        # Verify next day instances exist
        for i in range(3):
            new_tasks = [t for t in pet.get_required_tasks() 
                        if t.title == f"Task {i}" and not t.completion_status]
            assert len(new_tasks) == 1, f"Should have 1 incomplete Task {i}"


class TestConflictDetectionDuplicateTimes:
    """Comprehensive tests for conflict detection with duplicate times."""
    
    def test_detect_duplicate_required_times(self):
        """Verify scheduler flags multiple tasks scheduled at exact same time."""
        owner = Owner(name="Test", available_hours_per_day=8.0)
        pet = Pet(name="TestPet", species="dog", age=3)
        schedule = Schedule(owner=owner, pet=pet)
        
        # Create three tasks all at 9:00am
        task1 = Task(
            title="Walk",
            description="",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="9:00am"
        )
        
        task2 = Task(
            title="Feed",
            description="",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            required_time="9:00am"
        )
        
        task3 = Task(
            title="Medication",
            description="",
            duration_minutes=5,
            priority="high",
            task_type="medication",
            frequency="daily",
            required_time="9:00am"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        schedule.add_task(task1)
        schedule.add_task(task2)
        schedule.add_task(task3)
        
        # Simulate scheduling all at same time
        schedule.daily_plan = [
            (task1, "9:00am"),
            (task2, "9:00am"),
            (task3, "9:00am")
        ]
        
        conflicts = schedule.detect_conflicts()
        
        # Should detect multiple hard conflicts
        assert len(conflicts["hard"]) > 0, "Should detect conflicts at duplicate times"
        for conflict in conflicts["hard"]:
            assert "OVERLAP" in conflict, "Conflicts should specify overlap"
    
    def test_no_false_positives_off_by_one_minute(self):
        """Verify tasks with 1 minute gap are not flagged as conflicts."""
        owner = Owner(name="Test", available_hours_per_day=8.0)
        pet = Pet(name="TestPet", species="dog", age=3)
        schedule = Schedule(owner=owner, pet=pet)
        
        task1 = Task(
            title="Task A",
            description="",
            duration_minutes=30,
            priority="high",
            task_type="activity",
            frequency="daily"
        )
        
        task2 = Task(
            title="Task B",
            description="",
            duration_minutes=15,
            priority="high",
            task_type="activity",
            frequency="daily"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        schedule.add_task(task1)
        schedule.add_task(task2)
        
        # Schedule with 1 minute gap (no conflict)
        schedule.daily_plan = [
            (task1, "9:00am"),  # 9:00-9:30
            (task2, "9:31am")   # 9:31-9:46 (1 minute gap)
        ]
        
        conflicts = schedule.detect_conflicts(buffer_minutes=0)
        
        assert len(conflicts["hard"]) == 0, "1-minute gap should not be a hard conflict"
    
    def test_conflict_detection_with_zero_buffer(self):
        """Verify back-to-back tasks at exactly end time are not flagged."""
        owner = Owner(name="Test", available_hours_per_day=8.0)
        pet = Pet(name="TestPet", species="dog", age=3)
        schedule = Schedule(owner=owner, pet=pet)
        
        task1 = Task(
            title="First",
            description="",
            duration_minutes=30,
            priority="high",
            task_type="activity",
            frequency="daily"
        )
        
        task2 = Task(
            title="Second",
            description="",
            duration_minutes=15,
            priority="high",
            task_type="activity",
            frequency="daily"
        )
        
        schedule.daily_plan = [
            (task1, "9:00am"),  # 9:00-9:30
            (task2, "9:30am")   # 9:30-9:45 (exact boundary)
        ]
        
        conflicts = schedule.detect_conflicts(buffer_minutes=0)
        
        assert len(conflicts["hard"]) == 0, "Exact boundary should not conflict"
        assert len(conflicts["soft"]) == 0, "Zero buffer should allow exact boundaries"


# Helper function for time conversion tests
from pawpal_system import time_to_minutes
