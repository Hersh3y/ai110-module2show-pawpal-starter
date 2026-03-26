import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Initialize session state to persist Owner, Pet, and tasks across reruns
if 'owner' not in st.session_state:
    st.session_state.owner = None

if 'pet' not in st.session_state:
    st.session_state.pet = None

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Create Owner & Pet")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Create Owner & Pet"):
    # Wire to Owner class: instantiate a new Owner with the form data
    st.session_state.owner = Owner(
        name=owner_name,
        available_hours_per_day=4.0,
        preferred_activity_times=["morning", "evening"],
        preferences={}
    )
    
    # Wire to Pet class: instantiate a new Pet with the form data
    st.session_state.pet = Pet(
        name=pet_name,
        species=species,
        age=3,
        special_needs=[],
        care_requirements={}
    )
    
    # Wire to Owner.add_pet() method: add the pet to the owner
    st.session_state.owner.add_pet(st.session_state.pet)
    
    st.success(f"✅ Created: Owner '{owner_name}' with pet '{pet_name}' ({species})")

# Display current owner/pet if they exist (session state persists across reruns)
if st.session_state.owner and st.session_state.pet:
    st.info(f"📌 Owner: {st.session_state.owner.name} | Pet: {st.session_state.pet.name} ({st.session_state.pet.species})")


st.markdown("### Add Tasks to Pet")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.pet is None:
        st.error("❌ Please create an Owner & Pet first!")
    else:
        # Wire to Task class: instantiate a new Task with the form data
        new_task = Task(
            title=task_title,
            description=f"{task_title} for {st.session_state.pet.name}",
            duration_minutes=int(duration),
            priority=priority,
            task_type="activity",
            frequency="daily",
            required_time=None
        )
        
        # Wire to Pet.add_task() method: add the task to the pet
        st.session_state.pet.add_task(new_task)
        
        # Also update the display list for UI feedback
        st.session_state.tasks.append(
            {"title": task_title, "duration_minutes": int(duration), "priority": priority}
        )
        
        st.success(f"✅ Added task '{task_title}' to {st.session_state.pet.name}")


if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    # Validate that owner and pet exist, and that there are tasks
    if st.session_state.owner is None or st.session_state.pet is None:
        st.error("❌ Please create an Owner & Pet first!")
    elif len(st.session_state.pet.get_required_tasks()) == 0:
        st.error("❌ Please add at least one task!")
    else:
        # Wire to Schedule class: instantiate a Schedule with owner and pet
        schedule = Schedule(
            owner=st.session_state.owner,
            pet=st.session_state.pet,
            start_time="6:00am",
            end_time="10:00pm"
        )
        
        # Wire to Schedule.add_task(): add all tasks from the pet to the scheduler
        for task in st.session_state.pet.get_required_tasks():
            schedule.add_task(task)
        
        # Wire to Schedule.generate_schedule(): create the optimized plan
        schedule.generate_schedule()
        
        # Wire to Schedule.get_plan_with_reasoning(): display the results
        st.success("✅ Schedule generated successfully!")
        st.write(schedule.get_plan_with_reasoning())
        
        # Store in session state for potential future use/export
        st.session_state.current_schedule = schedule
