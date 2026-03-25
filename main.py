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
    
    # Add tasks to Mochi
    mochi.add_task(task_morning_walk)
    mochi.add_task(task_feeding_mochi)
    mochi.add_task(task_afternoon_walk)
    
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
