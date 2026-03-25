from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


def parse_time(time_str: str) -> datetime:
    """Parse time string like '9:00am' into datetime object."""
    return datetime.strptime(time_str, "%I:%M%p")


def time_to_minutes(time_str: str) -> int:
    """Convert time string like '9:00am' to minutes since midnight."""
    dt = parse_time(time_str)
    return dt.hour * 60 + dt.minute


def minutes_to_time(minutes: int) -> str:
    """Convert minutes since midnight back to time string like '9:00am'."""
    hours = minutes // 60
    mins = minutes % 60
    period = "am" if hours < 12 else "pm"
    hours_12 = hours if hours <= 12 else hours - 12
    if hours_12 == 0:
        hours_12 = 12
    return f"{hours_12}:{mins:02d}{period}"


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    description: str  # detailed description of the task
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    task_type: str  # "walk", "feed", "medication", "grooming", etc.
    frequency: str  # "daily", "weekly", "once", etc.
    required_time: Optional[str] = None  # e.g., "9:00am" for time-sensitive tasks
    completion_status: bool = False  # tracks whether task is completed
    dependencies: List[str] = field(default_factory=list)  # titles of tasks that must happen first

    def get_duration(self) -> int:
        """Returns duration of task in minutes."""
        return self.duration_minutes

    def is_urgent(self) -> bool:
        """Returns True if task is high priority or time-dependent."""
        return self.priority == "high" or self.required_time is not None

    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self.completion_status = True


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
        return self.tasks

    def add_task(self, task: Task) -> None:
        """Adds a task to this pet's task list."""
        self.tasks.append(task)

    def add_special_need(self, need: str) -> None:
        """Adds a special constraint or need for this pet."""
        if need not in self.special_needs:
            self.special_needs.append(need)

    def get_health_info(self) -> str:
        """Returns relevant health/care notes for this pet."""
        info = f"{self.name} is a {self.age}-year-old {self.species}.\n"
        if self.special_needs:
            info += f"Special needs: {', '.join(self.special_needs)}\n"
        return info.strip()


class Owner:
    """Represents the pet owner and their availability constraints."""

    def __init__(
        self,
        name: str,
        available_hours_per_day: float,
        preferred_activity_times: List[str] = None,
        preferences: Dict[str, Any] = None,
    ):
        """Initialize an owner with name, available hours, and preferences."""
        self.name = name
        self.available_hours_per_day = available_hours_per_day
        self.preferred_activity_times = preferred_activity_times or []
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_required_tasks())
        return all_tasks

    def get_available_time(self) -> float:
        """Returns available hours per day for pet care."""
        return self.available_hours_per_day

    def get_preference(self, key: str) -> Any:
        """Returns a preference value by key."""
        return self.preferences.get(key)

    def set_preference(self, key: str, value: Any) -> None:
        """Sets or updates a preference."""
        self.preferences[key] = value


class Schedule:
    """Orchestrates and generates the daily pet care plan."""

    def __init__(
        self,
        owner: Owner,
        pet: Pet,
        start_time: str = "6:00am",
        end_time: str = "10:00pm",
    ):
        """Initialize a schedule for an owner and pet with operating hours."""
        self.owner = owner
        self.pet = pet
        self.tasks: List[Task] = []
        self.daily_plan: List[tuple] = []  # list of (task, scheduled_time)
        self.start_time = start_time
        self.end_time = end_time
        self.start_minutes = time_to_minutes(start_time)
        self.end_minutes = time_to_minutes(end_time)

    def add_task(self, task: Task) -> None:
        """Adds a task to the available pool of tasks."""
        self.tasks.append(task)

    def _sort_tasks_by_priority(self) -> List[Task]:
        """Sorts tasks by urgency: urgent/high priority first, then by duration (longest first)."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        
        def sort_key(task):
            urgency = 1 if task.is_urgent() else 0
            priority_value = priority_map.get(task.priority, 0)
            # Sort by: urgency (desc), priority (desc), duration (desc)
            return (-urgency, -priority_value, -task.duration_minutes)
        
        return sorted(self.tasks, key=sort_key)

    def can_schedule_at(self, task: Task, time_minutes: int) -> bool:
        """Checks if a task can be scheduled at a given time (in minutes since midnight)."""
        task_end = time_minutes + task.get_duration()
        
        # Check if task fits within operating hours
        if time_minutes < self.start_minutes or task_end > self.end_minutes:
            return False
        
        # Check if time matches required_time (if specified)
        if task.required_time:
            required_minutes = time_to_minutes(task.required_time)
            if abs(time_minutes - required_minutes) > 30:  # Allow 30-min buffer
                return False
        
        # Check for conflicts with already scheduled tasks
        for scheduled_task, scheduled_time_str in self.daily_plan:
            scheduled_minutes = time_to_minutes(scheduled_time_str)
            scheduled_end = scheduled_minutes + scheduled_task.get_duration()
            
            # Check for overlap
            if (time_minutes < scheduled_end) and (task_end > scheduled_minutes):
                return False
        
        return True

    def generate_schedule(self) -> List[tuple]:
        """Generate optimized daily plan as a list of (task, scheduled_time) tuples."""
        self.daily_plan = []
        sorted_tasks = self._sort_tasks_by_priority()
        available_minutes = int(self.owner.get_available_time() * 60)
        time_elapsed = 0
        
        for task in sorted_tasks:
            # If task has required time, try to schedule it at that time
            if task.required_time:
                task_start_minutes = time_to_minutes(task.required_time)
                if self.can_schedule_at(task, task_start_minutes):
                    self.daily_plan.append((task, task.required_time))
                    continue
            
            # Otherwise, find the next available slot
            current_minutes = self.start_minutes
            for scheduled_task, scheduled_time_str in self.daily_plan:
                scheduled_start = time_to_minutes(scheduled_time_str)
                current_minutes = max(current_minutes, scheduled_start + scheduled_task.get_duration())
            
            # Try to fit the task in the next available slot
            if current_minutes + task.get_duration() <= self.end_minutes and time_elapsed + task.get_duration() <= available_minutes:
                scheduled_time = minutes_to_time(current_minutes)
                self.daily_plan.append((task, scheduled_time))
                time_elapsed += task.get_duration()
        
        return self.daily_plan

    def get_plan_with_reasoning(self) -> str:
        """Returns the daily plan with explanations of why each task was chosen and scheduled."""
        if not self.daily_plan:
            return "No schedule generated yet. Call generate_schedule() first."
        
        output = f"Daily Schedule for {self.pet.name}\n"
        output += f"Owner: {self.owner.name}\n"
        output += f"Available: {self.owner.get_available_time()} hours/day\n"
        output += "=" * 50 + "\n\n"
        
        for task, time_str in self.daily_plan:
            output += f"[{time_str}] {task.title} ({task.duration_minutes} min)\n"
            output += f"  Type: {task.task_type} | Priority: {task.priority}\n"
            if task.required_time:
                output += f"  Note: Time-sensitive (required at {task.required_time})\n"
            output += "\n"
        
        output += "=" * 50 + "\n"
        output += f"Total tasks scheduled: {len(self.daily_plan)}"
        
        return output

