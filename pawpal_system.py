from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, date


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
    task_date: Optional[datetime] = None  # tracks when this task instance is scheduled for

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

    def mark_task_complete(self, task_title: str) -> bool:
        """Marks a task as complete. If recurring, creates next instance.
        
        Uses timedelta to calculate the next occurrence date accurately:
        - Daily tasks: current_date + timedelta(days=1)
        - Weekly tasks: current_date + timedelta(days=7)
        
        Args:
            task_title: The title of the task to mark complete.
            
        Returns:
            bool: True if task was found and marked complete, False otherwise.
        """
        for task in self.tasks:
            if task.title == task_title:
                task.mark_complete()
                
                # If task is recurring, create a new instance for the next occurrence
                if task.frequency in ["daily", "weekly"]:
                    days_to_add = 1 if task.frequency == "daily" else 7
                    
                    # Calculate next occurrence date using timedelta
                    # If task_date exists, use it; otherwise use today's date
                    if task.task_date:
                        # Extract just the date part and add days
                        current_date = task.task_date if isinstance(task.task_date, date) else task.task_date.date()
                        next_date = datetime.combine(
                            current_date + timedelta(days=days_to_add),
                            datetime.min.time()
                        )
                    else:
                        # Use today's date and add the offset
                        today = datetime.now().date()
                        next_date = datetime.combine(
                            today + timedelta(days=days_to_add),
                            datetime.min.time()
                        )
                    
                    # Create new task instance for next occurrence
                    next_task = Task(
                        title=task.title,
                        description=task.description,
                        duration_minutes=task.duration_minutes,
                        priority=task.priority,
                        task_type=task.task_type,
                        frequency=task.frequency,
                        required_time=task.required_time,
                        completion_status=False,
                        dependencies=task.dependencies,
                        task_date=next_date
                    )
                    self.tasks.append(next_task)
                    return True
                
                return True
        
        return False

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

    def filter_tasks(self, 
                     pet_name: Optional[str] = None, 
                     completion_status: Optional[bool] = None) -> List[Task]:
        """Filters tasks by pet name and/or completion status.
        
        Args:
            pet_name: Optional pet name to filter by. If None, includes all pets.
            completion_status: Optional bool to filter by. 
                              True = completed tasks, False = incomplete, None = all.
        
        Returns:
            List[Task]: Filtered list of tasks matching the criteria.
        """
        filtered_tasks = []
        
        # Filter by pet name if specified
        if pet_name:
            for pet in self.pets:
                if pet.name == pet_name:
                    filtered_tasks.extend(pet.get_required_tasks())
        else:
            # Include all pets if no pet_name specified
            filtered_tasks = self.get_all_tasks()
        
        # Filter by completion status if specified
        if completion_status is not None:
            filtered_tasks = [task for task in filtered_tasks 
                            if task.completion_status == completion_status]
        
        return filtered_tasks

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

    def sort_by_time(self) -> List[Task]:
        """Sorts tasks by their required_time attribute (HH:MM format).
        
        Uses a lambda function to convert time strings to minutes for numeric comparison.
        Tasks with no required_time are placed at the end.
        
        Returns:
            List[Task]: Tasks sorted chronologically by required_time.
        """
        # Separate tasks with required_time from those without
        tasks_with_time = [task for task in self.tasks if task.required_time]
        tasks_without_time = [task for task in self.tasks if not task.required_time]
        
        # Sort tasks with required_time using lambda to convert time strings to minutes
        sorted_tasks_with_time = sorted(
            tasks_with_time,
            key=lambda task: time_to_minutes(task.required_time)
        )
        
        # Combine: time-sorted tasks first, then tasks without required_time
        return sorted_tasks_with_time + tasks_without_time

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

    def detect_conflicts(self, buffer_minutes: int = 5) -> Dict[str, List[str]]:
        """Detects scheduling conflicts in the daily plan.
        
        Identifies:
        - Hard conflicts: Tasks that directly overlap in time
        - Soft conflicts: Tasks with less than buffer_minutes between them
        
        Args:
            buffer_minutes: Minimum gap between tasks to avoid soft conflict warning.
            
        Returns:
            Dict with 'hard' and 'soft' keys, each containing list of conflict descriptions.
        """
        conflicts = {"hard": [], "soft": []}
        
        if not self.daily_plan:
            return conflicts
        
        # Create list of task events with their times
        task_events = []
        for idx, (task, time_str) in enumerate(self.daily_plan):
            start = time_to_minutes(time_str)
            end = start + task.duration_minutes
            task_events.append({
                "idx": idx,
                "title": task.title,
                "pet": self.pet.name,
                "start": start,
                "end": end
            })
        
        # Check each pair of tasks for conflicts
        for i in range(len(task_events)):
            for j in range(i + 1, len(task_events)):
                task_i = task_events[i]
                task_j = task_events[j]
                
                # Check for hard conflict (overlap)
                if task_i["start"] < task_j["end"] and task_i["end"] > task_j["start"]:
                    conflicts["hard"].append(
                        f"[OVERLAP] '{task_i['title']}' ({minutes_to_time(task_i['start'])}-"
                        f"{minutes_to_time(task_i['end'])}) overlaps with "
                        f"'{task_j['title']}' ({minutes_to_time(task_j['start'])}-"
                        f"{minutes_to_time(task_j['end'])})"
                    )
                
                # Check for soft conflict (tight gap)
                elif task_i["end"] <= task_j["start"]:
                    gap = task_j["start"] - task_i["end"]
                    if gap < buffer_minutes:
                        conflicts["soft"].append(
                            f"[TIGHT] Only {gap} min gap between '{task_i['title']}' "
                            f"(ends {minutes_to_time(task_i['end'])}) and "
                            f"'{task_j['title']}' (starts {minutes_to_time(task_j['start'])})"
                        )
        
        return conflicts

    def get_conflict_warnings(self, buffer_minutes: int = 5) -> List[str]:
        """Lightweight conflict detection that returns warning messages (non-fatal).
        
        Returns formatted warning strings for both hard and soft conflicts.
        Never crashes - catches errors and continues gracefully.
        
        Args:
            buffer_minutes: Minimum gap between tasks to trigger soft conflict warning.
            
        Returns:
            List[str]: Warning messages (empty if no conflicts).
        """
        warnings = []
        
        try:
            # Early exit: no tasks to check
            if not self.daily_plan or len(self.daily_plan) < 2:
                return warnings
            
            # Check each pair of consecutive and non-consecutive tasks
            for i in range(len(self.daily_plan)):
                for j in range(i + 1, len(self.daily_plan)):
                    try:
                        task_i, time_i_str = self.daily_plan[i]
                        task_j, time_j_str = self.daily_plan[j]
                        
                        # Skip if either task missing required_time
                        if not time_i_str or not time_j_str:
                            continue
                        
                        # Calculate times safely
                        start_i = time_to_minutes(time_i_str)
                        end_i = start_i + task_i.duration_minutes
                        start_j = time_to_minutes(time_j_str)
                        end_j = start_j + task_j.duration_minutes
                        
                        # Hard conflict: direct overlap
                        if start_i < end_j and end_i > start_j:
                            warnings.append(
                                f"⚠ CONFLICT: '{task_i.title}' and '{task_j.title}' "
                                f"overlap at {minutes_to_time(max(start_i, start_j))}"
                            )
                        
                        # Soft conflict: tasks back-to-back with tight gap
                        elif end_i <= start_j:
                            gap = start_j - end_i
                            if gap < buffer_minutes:
                                warnings.append(
                                    f"[WARN] WARNING: Only {gap}m between '{task_i.title}' "
                                    f"and '{task_j.title}' - tight scheduling"
                                )
                    
                    except (ValueError, TypeError) as e:
                        # Skip this pair if time parsing fails
                        continue
        
        except Exception as e:
            # Catch-all: never crashes, just log issue
            warnings.append(f"[ERROR] Could not fully analyze schedule: {str(e)}")
        
        return warnings

    def get_cross_pet_warnings(self, buffer_minutes: int = 5) -> List[str]:
        """Lightweight cross-pet conflict detection returning warning messages (non-fatal).
        
        Checks if owner can realistically manage multiple pets during their scheduled tasks.
        Never crashes - catches errors and continues gracefully.
        
        Args:
            buffer_minutes: Minimum gap between tasks for different pets.
            
        Returns:
            List[str]: Warning messages (empty if no cross-pet issues).
        """
        warnings = []
        
        try:
            # Early exit: only one pet
            if not self.owner.pets or len(self.owner.pets) < 2:
                return warnings
            
            # Collect active tasks with times across all pets
            pet_tasks = []
            for pet in self.owner.pets:
                for task in pet.get_required_tasks():
                    if task.required_time:
                        pet_tasks.append({
                            "pet": pet.name,
                            "title": task.title,
                            "start": time_to_minutes(task.required_time),
                            "end": time_to_minutes(task.required_time) + task.duration_minutes
                        })
            
            # Early exit: no tasks with times
            if len(pet_tasks) < 2:
                return warnings
            
            # Check for conflicts between different pets
            for i in range(len(pet_tasks)):
                for j in range(i + 1, len(pet_tasks)):
                    try:
                        t_i = pet_tasks[i]
                        t_j = pet_tasks[j]
                        
                        # Skip same pet
                        if t_i["pet"] == t_j["pet"]:
                            continue
                        
                        # Hard conflict: tasks overlap
                        if t_i["start"] < t_j["end"] and t_i["end"] > t_j["start"]:
                            warnings.append(
                                f"[CROSS-PET] CONFLICT: {t_i['pet']} ({t_i['title']}) "
                                f"overlaps with {t_j['pet']} ({t_j['title']}) at "
                                f"{minutes_to_time(max(t_i['start'], t_j['start']))}"
                            )
                        
                        # Soft conflict: tight gap between switching pets
                        elif t_i["end"] <= t_j["start"]:
                            gap = t_j["start"] - t_i["end"]
                            if gap < buffer_minutes:
                                warnings.append(
                                    f"[TIGHT] TRANSITION: Only {gap}m from {t_i['pet']} "
                                    f"to {t_j['pet']} - may be unrealistic"
                                )
                    
                    except (ValueError, TypeError, KeyError):
                        continue
        
        except Exception as e:
            warnings.append(f"[ERROR] Could not analyze cross-pet schedule: {str(e)}")
        
        return warnings

    def detect_cross_pet_conflicts(self, buffer_minutes: int = 5) -> Dict[str, List[str]]:
        """Detects scheduling conflicts across all pets for the same owner.
        
        Compares scheduled tasks across different pets to identify time conflicts
        that the owner would face (when managing multiple pets simultaneously).
        
        Args:
            buffer_minutes: Minimum gap between tasks to avoid soft conflict warning.
            
        Returns:
            Dict with 'hard' and 'soft' keys, each containing conflict descriptions.
        """
        conflicts = {"hard": [], "soft": []}
        
        if not self.owner.pets or len(self.owner.pets) < 2:
            return conflicts
        
        # Collect all scheduled tasks across all pets
        all_tasks = []
        for pet in self.owner.pets:
            for task in pet.get_required_tasks():
                if task.required_time:
                    all_tasks.append({
                        "title": task.title,
                        "pet": pet.name,
                        "start": time_to_minutes(task.required_time),
                        "end": time_to_minutes(task.required_time) + task.duration_minutes
                    })
        
        # Check each pair of tasks from different pets
        for i in range(len(all_tasks)):
            for j in range(i + 1, len(all_tasks)):
                task_i = all_tasks[i]
                task_j = all_tasks[j]
                
                # Only check if tasks are for different pets
                if task_i["pet"] == task_j["pet"]:
                    continue
                
                # Check for hard conflict (overlap)
                if task_i["start"] < task_j["end"] and task_i["end"] > task_j["start"]:
                    conflicts["hard"].append(
                        f"[CROSS-PET OVERLAP] Owner must manage '{task_i['title']}' ({task_i['pet']}) "
                        f"({minutes_to_time(task_i['start'])}-{minutes_to_time(task_i['end'])}) "
                        f"at same time as '{task_j['title']}' ({task_j['pet']}) "
                        f"({minutes_to_time(task_j['start'])}-{minutes_to_time(task_j['end'])})"
                    )
                
                # Check for soft conflict (tight gap)
                elif task_i["end"] <= task_j["start"]:
                    gap = task_j["start"] - task_i["end"]
                    if gap < buffer_minutes:
                        conflicts["soft"].append(
                            f"[CROSS-PET TIGHT] Only {gap} min to transition from "
                            f"'{task_i['title']}' ({task_i['pet']}, ends {minutes_to_time(task_i['end'])}) "
                            f"to '{task_j['title']}' ({task_j['pet']}, starts {minutes_to_time(task_j['start'])})"
                        )
        
        return conflicts

