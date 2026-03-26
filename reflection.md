# PawPal+ Project Reflection

## 1. System Design

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

**a. Initial design**

- Briefly describe your initial UML design.
    **Four classes: Owner (manages constraints), Pet (holds care requirements), Task (individual activities), and Schedule (generates the plan). Owner has Pets, Pets have Tasks, Schedule orchestrates and depends all three.**

- What classes did you include, and what responsibilities did you assign to each?
    **Owner: Represents the pet owner and their constraints. Responsibilities: track available hours per day, manage preferences, and provide constraints to the scheduler.

    Pet: Represents a pet and its care requirements. Responsibilities: store pet attributes (name, species, age, special needs), retrieve species-specific care requirements, and expose health/special need information.

    Task: Represents a single pet care activity. Responsibilities: define task properties (title, duration, priority, type), identify time-sensitive tasks, and track task dependencies.

    Schedule: Orchestrates the daily planning process. Responsibilities: accept a pool of tasks, generate an optimized schedule based on owner/pet constraints and task priorities, verify scheduling feasibility, and provide a readable plan with reasoning for each decision.**

**b. Design changes**

- Did your design change during implementation?
    **Yes. The initial design had Pet with a get_required_tasks() method that was unclear about what "required" meant (mandatory vs. all tasks).**

- If yes, describe at least one change and why you made it.
    **I added a tasks attribute to Pet to store all tasks directly, and added an add_task() method. This clarifies that Pet is responsible for managing its own task list. It makes it so that each specific pet has its own specific tasks.**

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    **The scheduler considers: (1) Operating hours (start_time, end_time), (2) Task priority, (3) Task urgency, (4) Owner's available hours per day, (5) Task duration, and (6) Conflict avoidance.**

- How did you decide which constraints mattered most?
    **I prioritized urgency first, then priority level, then duration (longer tasks scheduled in better slots). This ensures that critcal tasks are never missed.**

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    **The scheduler detects conflicts after the schedule generation and not DURING. This means the generate_schedule() method builds a plan without preventing conflicts, and then detect_conflicts() identifies problems after the fact.**

- Why is that tradeoff reasonable for this scenario?
    **It's a simpler design that separates schedule generation from validation and allows fast scheduling and multiple conflict detection strategies. The scheduler may generate invalid plans, but this is acceptable because pet care tasks are flexible, owners get warnings to adjust, and full optimization would be overkill for a daily plan.**

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    **I used AI for brainstorming scheduling algorithms, Implementing specific features like sort_by_time() with lambda functions, Designing conflict detection logic, Code review and optimization suggestions, Debugging time parsing edge cases.**

- What kinds of prompts or questions were most helpful?
    **Most helpful were specific, actionable prompts like "How would you implement sorting with lambda?" and "How could this algorithm be simplified?" and brainstorming prompts like "suggest scheduling algorithms" also provided good direction.**

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    **When reviewing sort_by_time(), AI suggested a more "Pythonic" version using tuple comparison: key=lambda task: (task.required_time is None, time_to_minutes(...) if task.required_time else 0). This was cleverer but less readable.**

- How did you evaluate or verify what the AI suggested?
    **I compared readability for future developers. The current version is less confusing and is immediately understandable. The Pythonic version that requires explaining due to its complexity.**

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    **Sorting tasks chronologically by time, Filtering tasks by pet name and completion status, Recurring daily/weekly task auto-creation with accurate date math, conflict detection**

- Why were these tests important?
    **These are the core features that the users rely on. Sorting and filtering ensure correct task retrieval. Conflict detection validates the schedule is usable. Testing both detailed and lightweight approaches ensures graceful error handling.**

**b. Confidence**

- How confident are you that your scheduler works correctly?
    **Very confident. All 28 tests pass including edge cases: empty task lists, malformed time strings, non-existent tasks, no conflicts, multiple conflicts. The lightweight warnings never crash even with bad input.**

- What edge cases would you test next if you had more time?
    **Tasks with 0-minute duration, owners with 0 available hours, timezone handling, tasks scheduled at midnight (00:00)**

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    **Seeing all 28 test cases pass.**

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    **Move conflict detection into generation (prevent invalid plans rather than just warn), Add constraint propagation for dependencies (if Task A must happen before Task B, prioritize it), Implement actual optimization algorithms, Add task flexibility.**

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    **Spending time planning a clear class design and backend logic prevents major problems later on. AI is most valuable for brainstorming and code validation, but maintaining human judgment about readability, simplicity, and architectural tradeoffs is essential.**
    
