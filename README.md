# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

### Core Task Management
- **Task Creation & Tracking** — Define pet care tasks with title, description, duration, priority, type, and frequency
- **Multi-Pet Management** — Organize and track tasks across multiple animals per owner
- **Completion Status Tracking** — Mark tasks as complete/incomplete with persistent state

### Intelligent Scheduling
- **Priority-Based Sorting** — Ranks tasks by urgency (time-sensitive first), priority level (high → medium → low), and duration (longest first)
- **Chronological Time Sorting** — Orders tasks by required time (e.g., "7:00am" before "12:00pm"); places flexible tasks at the end
- **Time-Slot Validation** — Respects operating hours (e.g., 6:00am–10:00pm) and owner availability constraints
- **Schedule Generation** — Builds an optimized daily plan that respects all constraints and time-sensitive requirements

### Flexible Task Filtering
- **Multi-Criteria Filtering** — Filter tasks by pet name, completion status, or both criteria combined
- **Aggregate Task Retrieval** — Fetch all tasks across all pets or specific subsets

### Recurring Task Management
- **Auto-Recurrence Creation** — Automatically spawns next instance of daily/weekly tasks when marked complete
- **Accurate Date Arithmetic** — Uses Python `timedelta` for precise date calculations (+1 day for daily, +7 days for weekly)
- **Property Preservation** — Recurring task instances inherit all properties (duration, priority, type, required time) from the original

### Conflict Detection & Warnings
- **Hard Conflict Detection** — Identifies directly overlapping scheduled tasks with time and duration details
- **Soft Conflict Detection** — Flags tasks with tight scheduling gaps (configurable buffer, default 5 minutes)
- **Lightweight Conflict Warnings** — Non-fatal warning system that gracefully handles time-parsing errors without crashing
- **Cross-Pet Scheduling** — Detects conflicts across multiple pets to ensure owner can realistically manage the full schedule

### Schedule Explanation
- **Plan with Reasoning** — Displays daily plan with time, duration, task type, and priority for each scheduled task
- **Human-Readable Output** — Formats schedule clearly with owner name, pet name, available hours, and total task count

## 📸 Demo

<a href="/course_images/ai110/demo.png" target="_blank"><img src='/course_images/ai110/demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Smarter Scheduling

PawPal+ implements sophisticated scheduling algorithms and conflict detection:

- **Priority-based Sorting**: Tasks sorted by urgency (time-sensitive first), priority level (high → medium → low), and duration
- **Task Filtering**: Filter tasks by pet, completion status, or both using flexible multi-criteria filtering
- **Recurring Task Auto-Creation**: Daily/weekly tasks automatically spawn the next occurrence when marked complete, using accurate date arithmetic with `timedelta`
- **Dual Conflict Detection**: 
  - Detailed analysis (dict-based) identifies hard conflicts (overlaps) and soft conflicts (tight scheduling gaps)
  - Lightweight warnings (string-based) provide non-fatal alerts that never crash, gracefully handling parsing errors
- **Cross-Pet Scheduling**: Detects conflicts across multiple pets, ensuring owner can realistically manage the entire schedule
- **Comprehensive Testing**: 21 test cases covering sorting, filtering, task completion, recurring creation, and both conflict detection strategies

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

### Run Tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite includes **28 comprehensive tests** across 6 test classes:

- **Sorting Correctness (5 tests)**: Verifies tasks are returned in strict chronological order, including edge cases like midnight boundaries and tasks without required times
- **Recurrence Logic (6 tests)**: Confirms daily/weekly recurring tasks create new instances with correct date increments using `timedelta`, and tests property preservation across recurrences
- **Conflict Detection - Duplicate Times (3 tests)**: Verifies the scheduler flags overlapping tasks and excludes false positives with 1-minute gaps and exact boundary conditions
- **Core Functionality (14 tests)**: Tests Task completion, Pet task management, Owner task filtering by pet/status, Schedule generation, hard/soft conflict detection, and cross-pet scheduling

**Key behaviors tested:**
- Empty lists and edge cases (midnight, all same time, no required times)
- Recurring task date arithmetic (+1 day for daily, +7 days for weekly)
- Property preservation when creating recurring task instances
- Multi-criteria filtering (pet name + completion status)
- Conflict detection accuracy with configurable buffers
- Non-recurring ("once") tasks don't spawn new instances

### Test Results

```
============================= 28 passed in 0.09s ==============================
```

### Confidence Level

**★★★★★ (5/5 stars)**

All 28 tests pass successfully. The test suite covers:
- ✅ Core functionality (task management, pet/owner operations)
- ✅ Critical scheduling logic (sorting, conflict detection)
- ✅ Recurring task edge cases (date arithmetic, property preservation)
- ✅ Boundary conditions (midnight transitions, zero-buffer scheduling)
- ✅ Multi-pet coordination (cross-pet conflict detection)

The system is **production-ready** for the core scheduling and conflict detection algorithms. The comprehensive edge-case coverage ensures robust behavior under real-world scheduling scenarios.
