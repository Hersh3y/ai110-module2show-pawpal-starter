from pawpal_system import Owner, Pet, Task, Schedule


def main():
    """Test script for PawPal+ system."""
    
    # Create an Owner
    owner = Owner(
        name="Harshal",
        available_hours_per_day=4.0,
        preferred_activity_times=["morning", "evening"],
        preferences={"avoid_after": "8pm"}
    )
    
    # Create Pet 1 - Dog (Mochi)
    mochi = Pet(
        name="Mochi",
        species="dog",
        age=3,
        special_needs=["energetic", "needs regular exercise"],
        care_requirements={"min_walks_per_day": 2, "water_breaks": 3}
    )
    
    # Create Pet 2 - Cat (Whiskers)
    whiskers = Pet(
        name="Whiskers",
        species="cat",
        age=5,
        special_needs=["picky eater", "sensitive to loud noises"],
        care_requirements={"meal_times": ["8:00am", "6:00pm"], "litter_changes": 1}
    )
    
    # Add Owner's pets
    owner.add_pet(mochi)
    owner.add_pet(whiskers)
    
    # Create tasks for Mochi (Dog)
    task_morning_walk = Task(
        title="Morning Walk",
        description="Take Mochi for a 30-minute walk around the park",
        duration_minutes=30,
        priority="high",
        task_type="walk",
        frequency="daily",
        required_time="7:00am"
    )
    
    task_feeding_mochi = Task(
        title="Mochi Feeding",
        description="Feed Mochi breakfast with kibble and fresh water",
        duration_minutes=15,
        priority="high",
        task_type="feed",
        frequency="daily",
        required_time="7:30am"
    )
    
    task_afternoon_walk = Task(
        title="Afternoon Walk",
        description="Take Mochi for another walk and playtime",
        duration_minutes=30,
        priority="medium",
        task_type="walk",
        frequency="daily"
    )
    
    # Create a task that conflicts with Morning Walk (same time)
    task_mochi_playtime = Task(
        title="Mochi Playtime",
        description="Interactive play session with Mochi",
        duration_minutes=20,
        priority="medium",
        task_type="enrichment",
        frequency="daily",
        required_time="7:00am"  # SAME TIME as Morning Walk - will create a hard conflict!
    )
    
    # Add tasks to Mochi
    mochi.add_task(task_morning_walk)
    mochi.add_task(task_feeding_mochi)
    mochi.add_task(task_afternoon_walk)
    mochi.add_task(task_mochi_playtime)  # This conflicts with Morning Walk
    
    # Create tasks for Whiskers (Cat)
    task_feeding_whiskers = Task(
        title="Whiskers Feeding (Breakfast)",
        description="Feed Whiskers her preferred wet food at breakfast",
        duration_minutes=10,
        priority="high",
        task_type="feed",
        frequency="daily",
        required_time="8:00am"
    )
    
    task_litter_change = Task(
        title="Litter Box Change",
        description="Clean and refresh Whiskers' litter box",
        duration_minutes=10,
        priority="medium",
        task_type="maintenance",
        frequency="daily"
    )
    
    task_playtime = Task(
        title="Playtime with Whiskers",
        description="Interactive play session with feather toy or laser pointer",
        duration_minutes=15,
        priority="low",
        task_type="enrichment",
        frequency="daily"
    )
    
    # Add tasks to Whiskers
    whiskers.add_task(task_feeding_whiskers)
    whiskers.add_task(task_litter_change)
    whiskers.add_task(task_playtime)
    
    # Mark some tasks as complete for demonstration
    task_morning_walk.mark_complete()
    task_playtime.mark_complete()
    
    # Print Owner and Pet Information
    print("\n" + "=" * 70)
    print("PawPal+ - TODAY'S SCHEDULE")
    print("=" * 70)
    print(f"\nOwner: {owner.name}")
    print(f"Available Time: {owner.get_available_time()} hours/day\n")
    
    # Display pet information
    for pet in owner.pets:
        print(f"\n{'-' * 70}")
        print(f"Pet: {pet.name}")
        print(f"{pet.get_health_info()}")
        print(f"Number of Tasks: {len(pet.get_required_tasks())}")
        print(f"{'-' * 70}")
        
        # Create a schedule for this pet
        schedule = Schedule(
            owner=owner,
            pet=pet,
            start_time="6:00am",
            end_time="10:00pm"
        )
        
        # Add all pet's tasks to the schedule
        for task in pet.get_required_tasks():
            schedule.add_task(task)
        
        # Generate and display the schedule
        schedule.generate_schedule()
        print(schedule.get_plan_with_reasoning())
        print()
    
    # Demonstrate SORTING by time
    print("\n" + "=" * 70)
    print("DEMONSTRATION: SORT_BY_TIME()")
    print("=" * 70)
    print("\nAll tasks sorted chronologically by required_time:\n")
    
    for pet in owner.pets:
        print(f"\n{pet.name}'s tasks sorted by time:")
        schedule = Schedule(owner=owner, pet=pet)
        for task in pet.get_required_tasks():
            schedule.add_task(task)
        
        sorted_tasks = schedule.sort_by_time()
        for idx, task in enumerate(sorted_tasks, 1):
            time_str = task.required_time if task.required_time else "No fixed time"
            print(f"  {idx}. [{time_str}] {task.title} ({task.duration_minutes} min)")
    
    # Demonstrate FILTERING by pet name
    print("\n" + "=" * 70)
    print("DEMONSTRATION: FILTER_TASKS() - By Pet Name")
    print("=" * 70)
    
    for pet_name in ["Mochi", "Whiskers"]:
        pet_tasks = owner.filter_tasks(pet_name=pet_name)
        print(f"\nAll tasks for {pet_name} ({len(pet_tasks)} total):")
        for idx, task in enumerate(pet_tasks, 1):
            status = "[DONE]" if task.completion_status else "[TODO]"
            print(f"  {idx}. {status} {task.title}")
    
    # Demonstrate FILTERING by completion status
    print("\n" + "=" * 70)
    print("DEMONSTRATION: FILTER_TASKS() - By Completion Status")
    print("=" * 70)
    
    incomplete_tasks = owner.filter_tasks(completion_status=False)
    print(f"\nIncomplete tasks ({len(incomplete_tasks)} total):")
    for idx, task in enumerate(incomplete_tasks, 1):
        print(f"  {idx}. {task.title} ({task.priority} priority)")
    
    completed_tasks = owner.filter_tasks(completion_status=True)
    print(f"\nCompleted tasks ({len(completed_tasks)} total):")
    for idx, task in enumerate(completed_tasks, 1):
        print(f"  {idx}. {task.title}")
    
    # Demonstrate FILTERING by both pet name AND completion status
    print("\n" + "=" * 70)
    print("DEMONSTRATION: FILTER_TASKS() - By Pet Name AND Completion Status")
    print("=" * 70)
    
    mochi_incomplete = owner.filter_tasks(pet_name="Mochi", completion_status=False)
    print(f"\nIncomplete tasks for Mochi ({len(mochi_incomplete)} total):")
    for idx, task in enumerate(mochi_incomplete, 1):
        print(f"  {idx}. {task.title}")
    
    whiskers_completed = owner.filter_tasks(pet_name="Whiskers", completion_status=True)
    print(f"\nCompleted tasks for Whiskers ({len(whiskers_completed)} total):")
    for idx, task in enumerate(whiskers_completed, 1):
        print(f"  {idx}. {task.title}")
    
    # Demonstrate CONFLICT DETECTION
    print("\n" + "=" * 70)
    print("DEMONSTRATION: CONFLICT DETECTION")
    print("=" * 70)
    
    # Check for conflicts within each pet's schedule
    print("\nConflict Detection for Individual Pet Schedules:")
    for pet in owner.pets:
        schedule = Schedule(owner=owner, pet=pet)
        for task in pet.get_required_tasks():
            if task.required_time:
                schedule.daily_plan.append((task, task.required_time))
        
        conflicts = schedule.detect_conflicts(buffer_minutes=5)
        
        print(f"\n{pet.name}'s Schedule:")
        if len(conflicts["hard"]) == 0 and len(conflicts["soft"]) == 0:
            print("  [OK] No conflicts detected")
        else:
            if conflicts["hard"]:
                print(f"  ✗ Hard Conflicts ({len(conflicts['hard'])}):")
                for conflict in conflicts["hard"]:
                    print(f"    - {conflict}")
            if conflicts["soft"]:
                print(f"  [SOFT] Conflicts ({len(conflicts['soft'])}):")
                for conflict in conflicts["soft"]:
                    print(f"    - {conflict}")
    
    # Demonstrate LIGHTWEIGHT warning approach (non-fatal)
    print(f"\n{'-' * 70}")
    print("Lightweight Conflict Warnings (Non-Fatal Approach):")
    
    for pet in owner.pets:
        schedule = Schedule(owner=owner, pet=pet)
        for task in pet.get_required_tasks():
            if task.required_time:
                schedule.daily_plan.append((task, task.required_time))
        
        # Use lightweight warning method - never crashes, returns simple strings
        warnings = schedule.get_conflict_warnings(buffer_minutes=5)
        
        print(f"\n{pet.name}'s Warnings:")
        if len(warnings) == 0:
            print("  [OK] No issues")
        else:
            for warning in warnings:
                print(f"  {warning}")
    
    # Check for cross-pet conflicts (owner managing multiple pets)
    print(f"\n{'-' * 70}")
    print("Cross-Pet Conflict Detection (Owner managing all pets):")
    
    schedule_multi = Schedule(owner=owner, pet=owner.pets[0])
    cross_conflicts = schedule_multi.detect_cross_pet_conflicts(buffer_minutes=5)
    
    if len(cross_conflicts["hard"]) == 0 and len(cross_conflicts["soft"]) == 0:
        print("  [OK] No cross-pet conflicts detected")
    else:
        if cross_conflicts["hard"]:
            print(f"  ✗ Cross-Pet Hard Conflicts ({len(cross_conflicts['hard'])}):")
            for conflict in cross_conflicts["hard"]:
                print(f"    - {conflict}")
        if cross_conflicts["soft"]:
            print(f"  [SOFT] Cross-Pet Conflicts ({len(cross_conflicts['soft'])}):")
            for conflict in cross_conflicts["soft"]:
                print(f"    - {conflict}")
    
    # Lightweight cross-pet warnings
    print(f"\n{'-' * 70}")
    print("Lightweight Cross-Pet Warnings (Non-Fatal):")
    
    cross_warnings = schedule_multi.get_cross_pet_warnings(buffer_minutes=5)
    
    if len(cross_warnings) == 0:
        print("  [OK] No cross-pet issues")
    else:
        for warning in cross_warnings:
            print(f"  {warning}")
    
    # Demonstrate RECURRING TASK creation
    print("\n" + "=" * 70)
    print("DEMONSTRATION: RECURRING TASK AUTO-CREATION")
    print("=" * 70)
    
    print(f"\nBefore completing 'Morning Walk' for Mochi:")
    print(f"  Total Mochi tasks: {len(mochi.get_required_tasks())}")
    for idx, t in enumerate(mochi.get_required_tasks(), 1):
        status = "[X]" if t.completion_status else "[ ]"
        date_str = f" (Date: {t.task_date.strftime('%Y-%m-%d')})" if t.task_date else ""
        print(f"    {idx}. [{status}] {t.title} - {t.frequency}{date_str}")
    
    # Mark the morning walk as complete - this should create a new daily instance
    print(f"\nMarking 'Morning Walk' as complete...")
    mochi.mark_task_complete("Morning Walk")
    
    print(f"\nAfter completing 'Morning Walk' for Mochi:")
    print(f"  Total Mochi tasks: {len(mochi.get_required_tasks())}")
    for idx, t in enumerate(mochi.get_required_tasks(), 1):
        status = "[✓]" if t.completion_status else "[ ]"
        date_str = f" (Date: {t.task_date.strftime('%Y-%m-%d') if t.task_date else 'N/A'})"
        print(f"    {idx}. [{status}] {t.title} - {t.frequency}{date_str}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    all_tasks = owner.get_all_tasks()
    print(f"Total tasks across all pets: {len(all_tasks)}")
    for pet in owner.pets:
        print(f"  - {pet.name}: {len(pet.get_required_tasks())} tasks")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
