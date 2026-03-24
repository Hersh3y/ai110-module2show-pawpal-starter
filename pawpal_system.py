from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    task_type: str  # "walk", "feed", "medication", "grooming", etc.
    required_time: Optional[str] = None  # e.g., "9:00am" for time-sensitive tasks
    dependencies: List[str] = field(default_factory=list)  # titles of tasks that must happen first

    def get_duration(self) -> int:
        """Returns duration of task in minutes."""
        pass

    def is_urgent(self) -> bool:
        """Returns True if task is high priority or time-dependent."""
        pass


@dataclass
class Pet:
    """Represents a pet and its care requirements."""
    name: str
    species: str  # "dog", "cat", "rabbit", etc.
    age: int
    special_needs: List[str] = field(default_factory=list)  # e.g., ["medication at 9am", "sensitive to heat"]
    care_requirements: Dict[str, Any] = field(default_factory=dict)  # species-specific defaults
    tasks: List[Task] = field(default_factory=list)  # all tasks associated with this pet

    def get_required_tasks(self) -> List[Task]:
        """Returns all tasks for this pet."""
        pass

    def add_task(self, task: Task) -> None:
        """Adds a task to this pet's task list."""
        pass

    def add_special_need(self, need: str) -> None:
        """Adds a special constraint or need for this pet."""
        pass

    def get_health_info(self) -> str:
        """Returns relevant health/care notes for this pet."""
        pass


class Owner:
    """Represents the pet owner and their availability constraints."""

    def __init__(
        self,
        name: str,
        available_hours_per_day: float,
        preferred_activity_times: List[str] = None,
        preferences: Dict[str, Any] = None,
    ):
        self.name = name
        self.available_hours_per_day = available_hours_per_day
        self.preferred_activity_times = preferred_activity_times or []
        self.preferences = preferences or {}

    def get_available_time(self) -> float:
        """Returns available hours per day for pet care."""
        pass

    def get_preference(self, key: str) -> Any:
        """Returns a preference value by key."""
        pass

    def set_preference(self, key: str, value: Any) -> None:
        """Sets or updates a preference."""
        pass


class Schedule:
    """Orchestrates and generates the daily pet care plan."""

    def __init__(
        self,
        owner: Owner,
        pet: Pet,
        start_time: str = "6:00am",
        end_time: str = "10:00pm",
    ):
        self.owner = owner
        self.pet = pet
        self.tasks: List[Task] = []
        self.daily_plan: List[Task] = []
        self.start_time = start_time
        self.end_time = end_time

    def add_task(self, task: Task) -> None:
        """Adds a task to the available pool of tasks."""
        pass

    def generate_schedule(self) -> List[Task]:
        """Creates an optimized daily plan based on constraints and priorities."""
        pass

    def can_schedule_at(self, task: Task, time: str) -> bool:
        """Checks if a task can be scheduled at a given time."""
        pass

    def get_plan_with_reasoning(self) -> str:
        """Returns the daily plan with explanations of why each task was chosen and scheduled."""
        pass
