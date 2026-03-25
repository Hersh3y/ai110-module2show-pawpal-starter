import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import pawpal_system
sys.path.insert(0, str(Path(__file__).parent.parent))

from pawpal_system import Task, Pet, Owner


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
