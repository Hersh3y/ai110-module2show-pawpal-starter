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
            required_time="7:10am"  # Overlaps with Mochi's walk
        )
        
        pet1.add_task(task1)
        pet2.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet1)
        
        conflicts = schedule.detect_cross_pet_conflicts()
        
        assert len(conflicts["hard"]) > 0, "Should have cross-pet hard conflict"
        assert "CROSS-PET OVERLAP" in conflicts["hard"][0], "Should mention cross-pet conflict"
    
    def test_cross_pet_soft_conflict(self):
        """Verify that tight gaps in cross-pet tasks are detected."""
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
        
        # Task for Mochi ending at 7:30
        task1 = Task(
            title="Mochi Walk",
            description="Dog walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        # Task for Whiskers starting at 7:33 (only 3 minute gap)
        task2 = Task(
            title="Whiskers Feed",
            description="Cat feeding",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            required_time="7:33am"
        )
        
        pet1.add_task(task1)
        pet2.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet1)
        
        conflicts = schedule.detect_cross_pet_conflicts(buffer_minutes=5)
        
        assert len(conflicts["soft"]) > 0, "Should have cross-pet soft conflict"
        assert "CROSS-PET TIGHT" in conflicts["soft"][0], "Should mention cross-pet tight gap"
    
    def test_no_cross_pet_conflict_for_single_pet(self):
        """Verify that single pet doesn't trigger cross-pet conflicts."""
        owner = Owner(
            name="Harshal",
            available_hours_per_day=8.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        pet = Pet(name="Mochi", species="dog", age=3, special_needs=[], care_requirements={})
        owner.add_pet(pet)
        
        task = Task(
            title="Walk",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        pet.add_task(task)
        
        schedule = Schedule(owner=owner, pet=pet)
        
        conflicts = schedule.detect_cross_pet_conflicts()
        
        assert len(conflicts["hard"]) == 0, "Should have no cross-pet conflicts with single pet"
        assert len(conflicts["soft"]) == 0, "Should have no cross-pet conflicts with single pet"


class TestLightweightWarnings:
    """Tests for lightweight conflict warning methods (non-fatal)."""
    
    def test_get_conflict_warnings_no_conflicts(self):
        """Verify lightweight warnings returns empty list when no conflicts."""
        owner = Owner(
            name="Harshal",
            available_hours_per_day=8.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        pet = Pet(name="Mochi", species="dog", age=3, special_needs=[], care_requirements={})
        owner.add_pet(pet)
        
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
            title="Feed",
            description="Feed",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            required_time="8:00am"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet)
        schedule.daily_plan = [(task1, "7:00am"), (task2, "8:00am")]
        
        warnings = schedule.get_conflict_warnings()
        
        assert isinstance(warnings, list), "Should return a list"
        assert len(warnings) == 0, "Should have no warnings"
    
    def test_get_conflict_warnings_with_overlap(self):
        """Verify lightweight warnings detects overlapping tasks."""
        owner = Owner(
            name="Harshal",
            available_hours_per_day=8.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        pet = Pet(name="Mochi", species="dog", age=3, special_needs=[], care_requirements={})
        owner.add_pet(pet)
        
        task1 = Task(
            title="Walk 1",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        task2 = Task(
            title="Walk 2",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:15am"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet)
        schedule.daily_plan = [(task1, "7:00am"), (task2, "7:15am")]
        
        warnings = schedule.get_conflict_warnings()
        
        assert len(warnings) > 0, "Should detect overlap warning"
        assert "CONFLICT" in warnings[0], "Warning should mention conflict"
    
    def test_get_conflict_warnings_graceful_error_handling(self):
        """Verify lightweight warnings never crashes with bad input."""
        owner = Owner(
            name="Harshal",
            available_hours_per_day=8.0,
            preferred_activity_times=["morning"],
            preferences={}
        )
        
        pet = Pet(name="Mochi", species="dog", age=3, special_needs=[], care_requirements={})
        owner.add_pet(pet)
        
        schedule = Schedule(owner=owner, pet=pet)
        
        # Intentionally bad time format
        task = Task(
            title="Walk",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        schedule.daily_plan = [(task, "INVALID_TIME"), (task, "7:00am")]
        
        # Should not crash - just skip the invalid pair
        warnings = schedule.get_conflict_warnings()
        
        assert isinstance(warnings, list), "Should always return a list"
        # May have warning about invalid time or may skip pair
    
    def test_get_cross_pet_warnings_no_conflicts(self):
        """Verify cross-pet lightweight warnings work without conflicts."""
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
        
        task1 = Task(
            title="Mochi Walk",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        task2 = Task(
            title="Whiskers Feed",
            description="Feed",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            required_time="9:00am"
        )
        
        pet1.add_task(task1)
        pet2.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet1)
        
        warnings = schedule.get_cross_pet_warnings()
        
        assert isinstance(warnings, list), "Should return a list"
        assert len(warnings) == 0, "Should have no cross-pet warnings"
    
    def test_get_cross_pet_warnings_with_overlap(self):
        """Verify cross-pet lightweight warnings detects conflicts."""
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
        
        task1 = Task(
            title="Mochi Walk",
            description="Walk",
            duration_minutes=30,
            priority="high",
            task_type="walk",
            frequency="daily",
            required_time="7:00am"
        )
        
        task2 = Task(
            title="Whiskers Feed",
            description="Feed",
            duration_minutes=15,
            priority="high",
            task_type="feed",
            frequency="daily",
            required_time="7:10am"  # Overlaps with Mochi's walk
        )
        
        pet1.add_task(task1)
        pet2.add_task(task2)
        
        schedule = Schedule(owner=owner, pet=pet1)
        
        warnings = schedule.get_cross_pet_warnings()
        
        assert len(warnings) > 0, "Should detect cross-pet conflict"
        assert "CROSS-PET" in warnings[0], "Should mention cross-pet in warning"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
