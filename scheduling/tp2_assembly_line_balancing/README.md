# TP2: Resource-Constrained Assembly Line Balancing (RC-ALBP)

## Overview

This practical work (TP) focuses on a simplified variant of Assembly Line Balancing that combines:
- **SALBP-2** (Simple Assembly Line Balancing - Type 2): Minimize cycle time with fixed stations
- **Resource constraints**: Tasks consume resources that are allocated to workstations


## The Assembly Line Concept

### Why "Cycle Time" Matters

An assembly line is **repetitive** - products (e.g., aircraft, cars) flow through stations continuously.

**Key concept:** At any moment in time, **multiple products are being worked on simultaneously**, each at a different station. Every **cycle time** units, all products shift one station to the right: a new product enters, and a finished product exits.

**The bottleneck station determines the cycle time** - all stations must finish their work within this time window before the next shift happens.

### Visual Example: Aircraft Assembly Line Flow

**Step 1 - Understanding the flow (3 stations, cycle time = 9):**

<table>
<tr><th colspan="3">Period 0 (t=0 to t=9)</th></tr>
<tr>
  <td align="center"><b>Station A</b><br/>✈️1<br/>(9 time)</td>
  <td align="center"><b>Station B</b><br/>✈️2<br/>(8 time)</td>
  <td align="center"><b>Station C</b><br/>✈️3<br/>(6 time)</td>
</tr>
<tr><td colspan="3" align="center">← <b>3 aircraft in parallel</b> →</td></tr>
</table>

**After 9 time units → SHIFT RIGHT → New aircraft enters, Finished aircraft exits**

<table>
<tr><th colspan="3">Period 1 (t=9 to t=18)</th></tr>
<tr>
  <td align="center"><b>Station A</b><br/>✈️4<br/>(new!)</td>
  <td align="center"><b>Station B</b><br/>✈️1<br/>(moved →)</td>
  <td align="center"><b>Station C</b><br/>✈️2<br/>(moved →)</td>
</tr>
<tr><td colspan="3" align="center">← <b>Everything shifted right!</b> → ✈️3 DONE! ✓</td></tr>
</table>

<table>
<tr><th colspan="3">Period 2 (t=18 to t=27)</th></tr>
<tr>
  <td align="center"><b>Station A</b><br/>✈️5<br/>(new!)</td>
  <td align="center"><b>Station B</b><br/>✈️4<br/>(moved →)</td>
  <td align="center"><b>Station C</b><br/>✈️1<br/>(moved →)</td>
</tr>
<tr><td colspan="3" align="center">← <b>Continuous flow</b> → ✈️2 DONE! ✓</td></tr>
</table>

**Step 2 - What happens INSIDE each station during one cycle (t=0 to t=9):**

<table border="1">
<tr>
  <th>Station A (working on ✈️1)</th>
  <th>t=0</th><th>t=1</th><th>t=2</th><th>t=3</th><th>t=4</th>
  <th>t=5</th><th>t=6</th><th>t=7</th><th>t=8</th>
</tr>
<tr>
  <td><b>Prepare</b> (5 units)</td>
  <td bgcolor="#99ccff"><b>Prepare</b></td>
  <td bgcolor="#99ccff"><b>Prepare</b></td>
  <td bgcolor="#99ccff"><b>Prepare</b></td>
  <td bgcolor="#99ccff"><b>Prepare</b></td>
  <td bgcolor="#99ccff"><b>Prepare</b></td>
  <td>—</td><td>—</td><td>—</td><td>—</td>
</tr>
<tr>
  <td><b>Cut</b> (4 units)</td>
  <td>—</td><td>—</td><td>—</td><td>—</td><td>—</td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
</tr>
<tr><td colspan="10"><b>Total: 9 time units</b> (sequential - precedence constraint: Prepare → Cut)</td></tr>
</table>

<table border="1">
<tr>
  <th>Station B (working on ✈️2)</th>
  <th>t=0</th><th>t=1</th><th>t=2</th><th>t=3</th><th>t=4</th>
  <th>t=5</th><th>t=6</th><th>t=7</th><th>t=8</th>
</tr>
<tr>
  <td><b>Assemble</b> (3 units)</td>
  <td bgcolor="#99ccff"><b>Assemble</b></td>
  <td bgcolor="#99ccff"><b>Assemble</b></td>
  <td bgcolor="#99ccff"><b>Assemble</b></td>
  <td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td>
</tr>
<tr>
  <td><b>Join</b> (3 units)</td>
  <td>—</td><td>—</td><td>—</td>
  <td bgcolor="#ffcc99"><b>Join</b></td>
  <td bgcolor="#ffcc99"><b>Join</b></td>
  <td bgcolor="#ffcc99"><b>Join</b></td>
  <td>—</td><td>—</td><td>—</td>
</tr>
<tr>
  <td><b>Test</b> (2 units)</td>
  <td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td>
  <td bgcolor="#b3ff99"><b>Test</b></td>
  <td bgcolor="#b3ff99"><b>Test</b></td>
  <td>—</td>
</tr>
<tr><td colspan="10"><b>Total: 8 time units</b> (1 idle unit) - sequential due to precedences</td></tr>
</table>

<table border="1">
<tr>
  <th>Station C (working on ✈️3)</th>
  <th>t=0</th><th>t=1</th><th>t=2</th><th>t=3</th><th>t=4</th>
  <th>t=5</th><th>t=6</th><th>t=7</th><th>t=8</th>
</tr>
<tr>
  <td><b>Package</b> (6 units)</td>
  <td bgcolor="#99ccff"><b>Package</b></td>
  <td bgcolor="#99ccff"><b>Package</b></td>
  <td bgcolor="#99ccff"><b>Package</b></td>
  <td bgcolor="#99ccff"><b>Package</b></td>
  <td bgcolor="#99ccff"><b>Package</b></td>
  <td bgcolor="#99ccff"><b>Package</b></td>
  <td>—</td><td>—</td><td>—</td>
</tr>
<tr><td colspan="10"><b>Total: 6 time units</b> (3 idle units)</td></tr>
</table>

**Result:** Cycle Time = max(9, 8, 6) = **9 time units**
**Throughput:** 1 aircraft every 9 time units

**Key insight:** The assembly line is a **pipeline**. Once in steady state, you complete one aircraft every 9 time units (the cycle time), even though each aircraft takes 27 time units total to fully complete (passing through 3 stations × 9 time units per cycle).

**Important:** Tasks shown above are sequential due to precedence constraints. However, **tasks CAN overlap** if:
- ✓ No precedence constraint between them
- ✓ Combined resource usage ≤ station capacity

*Example:* If Station_B had two independent tasks "Polish" (2 units, 1 Worker) and "Label" (2 units, 1 Worker), and the station has 2 Workers, they could run in parallel from t=0 to t=2, completing in 2 time units instead of 4!

### The Optimization Problem

<table border="1">
<tr bgcolor="#e6f7ff"><th colspan="2" style="color:black"><b>🎯 OPTIMIZATION GOAL</b></th></tr>
<tr>
  <td><b>Objective</b></td>
  <td><b>Minimize Cycle Time</b> (maximize throughput)</td>
</tr>
<tr>
  <td><b>Decision Variables</b></td>
  <td>
    1. <b>Allocation decisions:</b> Assignment of tasks to stations<br>
    2. <b>Temporal decisions:</b> Timing of task execution
  </td>
</tr>
</table>

<table border="1">
<tr bgcolor="#fff7e6"><th colspan="2" style="color:black"><b>⚙️ CONSTRAINTS</b></th></tr>
<tr>
  <td><b>1. Precedence</b></td>
  <td>
    If task A → task B in precedence graph:<br>
    • Station precedence: station[A] ≤ station[B]<br>
    • Temporal precedence (same station): end[A] ≤ start[B]
  </td>
</tr>
<tr>
  <td><b>2. Resources</b></td>
  <td>
    Cumulative resource capacity per station:<br>
    At any time t, sum of resources used by active tasks ≤ station capacity<br>
    <b>⭐ Tasks CAN overlap if combined resource usage stays within limits!</b>
  </td>
</tr>
</table>

**Example Comparison:**

<table border="1">
<tr>
  <th>Scenario</th>
  <th>Station A</th>
  <th>Station B</th>
  <th>Station C</th>
  <th>Cycle Time</th>
  <th>Result</th>
</tr>
<tr bgcolor="#ffe6e6">
  <td style="color:black"><b>❌ Bad Balancing</b></td>
  <td style="color:black"><b>15 time units<br>← BOTTLENECK!</b></td>
  <td style="color:black"><b>5 time units<br>(10 idle)</b></td>
  <td style="color:black"><b>3 time units<br>(12 idle)</b></td>
  <td style="color:black"><b>15</b></td>
  <td style="color:black"><b>Poor utilization<br>Low throughput</b></td>
</tr>
<tr bgcolor="#e6f7ff">
  <td style="color:black"><b>✓ Good Balancing</b></td>
  <td style="color:black"><b>10 time units</b></td>
  <td style="color:black"><b>9 time units</b></td>
  <td style="color:black"><b>10 time units</b></td>
  <td style="color:black"><b>10</b></td>
  <td style="color:black"><b>Well balanced<br>Higher throughput</b></td>
</tr>
<tr bgcolor="#e6ffe6">
  <td style="color:black"><b>✓ With Task Overlap</b></td>
  <td style="color:black"><b>8 time units<br>(2 tasks parallel)</b></td>
  <td style="color:black"><b>7 time units<br>(overlap allowed)</b></td>
  <td style="color:black"><b>8 time units</b></td>
  <td style="color:black"><b>8</b></td>
  <td style="color:black"><b>Best! Overlapping<br>independent tasks</b></td>
</tr>
</table>

**Key Insight:** By allowing tasks to overlap (when resources permit and no precedence conflicts), you can achieve even better cycle times than sequential execution!

### Precedence Constraints

Tasks must respect **two types** of precedence:

**1. STATION PRECEDENCE (Between stations):**

<table border="1">
<tr>
  <th>Station A</th>
  <th></th>
  <th>Station B</th>
  <th></th>
  <th>Station C</th>
</tr>
<tr align="center">
  <td><b>Prepare</b></td>
  <td>→</td>
  <td><b>Assemble</b></td>
  <td>→</td>
  <td><b>Test</b></td>
</tr>
</table>

**Rule:** If task A → task B in precedence graph, and they are assigned to different stations, then `station[A] ≤ station[B]`

This ensures tasks flow forward through the assembly line.

**2. TEMPORAL PRECEDENCE (Within same station):**

<table border="1">
<tr>
  <th colspan="10">Station A (time axis →)</th>
</tr>
<tr align="center">
  <td colspan="5"><b>Prepare</b></td>
  <td colspan="4"><b>Cut</b></td>
  <td></td>
</tr>
<tr align="center">
  <td>0</td>
  <td>1</td>
  <td>2</td>
  <td>3</td>
  <td>4</td>
  <td>5</td>
  <td>6</td>
  <td>7</td>
  <td>8</td>
  <td>9</td>
</tr>
</table>

**Rule:** If tasks A and B are on the **same station** AND A → B in precedence graph, then `end_time[A] ≤ start_time[B]`

This prevents overlapping tasks that have dependencies.

### Resource Constraints

Each station has **pre-allocated resources**, tasks consume resources:

<table border="1">
<tr bgcolor="#e6f7ff">
  <th style="color:black"><b>Station</b></th>
  <th style="color:black"><b>Worker Capacity</b></th>
  <th style="color:black"><b>Tool Capacity</b></th>
</tr>
<tr>
  <td><b>Station_A</b></td>
  <td><b>3 units</b></td>
  <td><b>2 units</b></td>
</tr>
<tr>
  <td><b>Station_B</b></td>
  <td><b>2 units</b></td>
  <td><b>3 units</b></td>
</tr>
</table>

<table border="1">
<tr bgcolor="#fff7e6">
  <th style="color:black"><b>Task</b></th>
  <th style="color:black"><b>Worker Consumption</b></th>
  <th style="color:black"><b>Tool Consumption</b></th>
</tr>
<tr><td><b>Prepare</b></td><td><b>1</b></td><td><b>0</b></td></tr>
<tr><td><b>Cut</b></td><td><b>1</b></td><td><b>1</b></td></tr>
<tr><td><b>Polish</b></td><td><b>1</b></td><td><b>0</b></td></tr>
</table>

**Constraint Rule:** At any time t, sum of resources used by active tasks on a station ≤ station's resource capacity

**Visual Examples:**

<table border="1">
<tr><th colspan="11">Example 1: Sequential Execution (Station has 1 Worker, 1 Tool)</th></tr>
<tr>
  <td><b>Task</b></td>
  <td><b>t=0</b></td><td><b>t=1</b></td><td><b>t=2</b></td><td><b>t=3</b></td><td><b>t=4</b></td>
  <td><b>t=5</b></td><td><b>t=6</b></td><td><b>t=7</b></td><td><b>t=8</b></td><td><b>Result</b></td>
</tr>
<tr>
  <td>Prepare [1W,0T]</td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td>—</td><td>—</td><td>—</td><td>—</td>
  <td>✓ OK</td>
</tr>
<tr>
  <td>Cut [1W,1T]</td>
  <td>—</td><td>—</td><td>—</td><td>—</td><td>—</td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td>✓ OK</td>
</tr>
<tr><td colspan="11"><b>Sequential:</b> Prepare (5 units) then Cut (4 units) → Total time: 9 units</td></tr>
</table>

<table border="1">
<tr><th colspan="11">Example 2: ❌ Same Tasks, Overlapping NOT Allowed (Still 1 Worker, 1 Tool)</th></tr>
<tr>
  <td><b>Task</b></td>
  <td><b>t=0</b></td><td><b>t=1</b></td><td><b>t=2</b></td><td><b>t=3</b></td><td><b>t=4</b></td>
  <td><b>t=5</b></td><td><b>t=6</b></td><td><b>t=7</b></td><td><b>t=8</b></td><td><b>Result</b></td>
</tr>
<tr>
  <td>Prepare [1W,0T]</td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#ff9999"><b>Prep</b></td>
  <td bgcolor="#ff9999"><b>Prep</b></td>
  <td>—</td><td>—</td><td>—</td><td>—</td>
  <td rowspan="2" bgcolor="#ffcccc" style="color:black"><b>✗ VIOLATION!</b><br>At t=3 to t=4:<br>Need 2W, 1T<br>Have 1W, 1T</td>
</tr>
<tr>
  <td>Cut [1W,1T]</td>
  <td>—</td><td>—</td><td>—</td>
  <td bgcolor="#ff9999"><b>Cut</b></td>
  <td bgcolor="#ff9999"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td>—</td><td>—</td>
</tr>
<tr><td colspan="11"><b>Attempted overlap (red) → EXCEEDS Worker capacity!</b> Cannot start Cut early.</td></tr>
</table>

<table border="1">
<tr><th colspan="11">Example 3: ✓ Same Tasks, Overlapping IS Allowed (Now 2 Workers, 1 Tool)</th></tr>
<tr>
  <td><b>Task</b></td>
  <td><b>t=0</b></td><td><b>t=1</b></td><td><b>t=2</b></td><td><b>t=3</b></td><td><b>t=4</b></td>
  <td><b>t=5</b></td><td><b>t=6</b></td><td><b>t=7</b></td><td><b>t=8</b></td><td><b>Result</b></td>
</tr>
<tr>
  <td>Prepare [1W,0T]</td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ccff"><b>Prep</b></td>
  <td bgcolor="#99ff99"><b>Prep</b></td>
  <td bgcolor="#99ff99"><b>Prep</b></td>
  <td>—</td><td>—</td><td>—</td><td>—</td>
  <td rowspan="2" bgcolor="#ccffcc" style="color:black"><b>✓ VALID!</b><br>At t=3 to t=4:<br>Need 2W, 1T<br>Have 2W, 1T</td>
</tr>
<tr>
  <td>Cut [1W,1T]</td>
  <td>—</td><td>—</td><td>—</td>
  <td bgcolor="#99ff99"><b>Cut</b></td>
  <td bgcolor="#99ff99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td bgcolor="#ffcc99"><b>Cut</b></td>
  <td>—</td><td>—</td>
</tr>
<tr><td colspan="11"><b>Parallel execution (green) → Total time: 7 units instead of 9!</b> With 2 Workers, overlap allowed.</td></tr>
</table>

**Key Takeaway:** The CP-SAT solver uses `AddCumulative` constraints to allow task overlapping when resource capacity permits, potentially reducing cycle time significantly!
## Problem Definition

### Given
- A fixed number of **workstations** (stations)
- A set of **tasks** with processing times
- **Precedence constraints** between tasks
- Multiple **resource types** (e.g., workers, tools, space)
- **Resource allocation** to each workstation (pre-decided)
- **Resource consumption** by each task

### Decision Variables
- **Task assignment**: Which station executes which task?
- **Task schedule**: When does each task start within the cycle?

### Objective
**Minimize the cycle time** (makespan) - the maximum completion time across all stations

### Constraints
1. **Precedence**: Predecessor tasks must complete before successors, or allocated to a previous station
2. **Resource capacity**: Resource consumption at each station cannot exceed allocation

## Files

### Core Problem Classes
- **`problem.py`**: Problem and solution classes following discrete-optimization API
  - `RCALBPProblem`: Inherits from `SchedulingProblem[Task]` and `AllocationProblem[Task, Station]`
  - `RCALBPSolution`: Implements both `SchedulingSolution` and `AllocationSolution` interfaces

### Utilities
- **`utils.py`**: Helper functions
  - `create_simple_instance()`: Generate random instances
  - `create_precedence_example()`: Small example with meaningful names
  - `create_from_rcpsp()`: Convert RCPSP to RC-ALBP with tighter resource constraints
  - `load_rcpsp_as_albp()`: Load realistic instances from PSPLib
  - `visualize_solution()`: Static Gantt chart visualization
  - `visualize_interactive_flow()`: **Interactive assembly line flow animation with time slider** ✨
    - Shows products flowing through stations over time
    - Tracks active tasks and resource usage per station
    - Highlights constraint violations in real-time
  - `print_solution_info()`: Detailed solution analysis

### Tutorial and Exercises
- **`tutorial.py`**: Interactive walkthrough (run this first!)
- **`exercises.py`**: CP-SAT solver implementation with interactive visualization
- **`solutions.py`**: Complete reference implementation with visualization demo
- **`benchmark.py`**: Comprehensive performance analysis ✨
  - Tests multiple instances with varying station counts
  - Generates 6 analysis plots (cycle time vs stations, solve time, optimality rates, etc.)
  - Creates interactive flow visualization demo
  - Exports results to CSV and PNG

## How to Run

```bash
# From the repo root (aibt_108/)

# 1. Run the tutorial (start here!)
uv run python -m scheduling.tp2_assembly_line_balancing.tutorial

# 2. View exercises instructions
uv run python -m scheduling.tp2_assembly_line_balancing.exercises

# 3. Test realistic instance creation from RCPSP
uv run python -c "
from scheduling.tp2_assembly_line_balancing.utils import load_rcpsp_as_albp
problem = load_rcpsp_as_albp('j301_1', nb_stations=3)
print(f'Loaded: {problem.nb_tasks} tasks, {problem.nb_stations} stations')
"

# 4. Run benchmark suite (after implementing solver!)
uv run python -m scheduling.tp2_assembly_line_balancing.benchmark
```

## Example Problem

The tutorial uses a small example with **meaningful names**:

### Tasks
- **Prepare** (5 time units)
- **Assemble** (3 time units)
- **Cut** (4 time units)
- **Join** (3 time units)
- **Test** (2 time units)
- **Package** (6 time units)

### Precedence Structure
```
Prepare → Assemble → Test
   ↓         ↓        ↓
  Cut   →  Join  → Package
```

### Stations
- **Station_A**
- **Station_B**

### Resources
- **Worker**: 3 units at Station_A, 2 units at Station_B
- **Tool**: 2 units at Station_A, 3 units at Station_B

### Task Resource Consumption
- **Prepare**: 1 Worker
- **Assemble**: 1 Tool
- **Cut**: 1 Worker, 1 Tool
- **Join**: 1 Tool
- **Test**: 1 Worker, 1 Tool
- **Package**: 2 Workers, 1 Tool

## Key Design Choices

### 1. Hashable Identifiers
Tasks, Stations, and Resources can be **strings or integers** for better readability:
```python
# Meaningful names (recommended for clarity)
tasks = ["Prepare", "Assemble", "Cut"]
stations = ["Station_A", "Station_B"]
resources = ["Worker", "Tool"]

# Or simple identifiers
tasks = ["T1", "T2", "T3"]
stations = ["WS1", "WS2"]
resources = ["R1", "R2"]
```

### 2. Discrete-Optimization Framework
Follows the library's design patterns:
- `SchedulingProblem[Task]`: Provides scheduling methods
- `AllocationProblem[Task, Station]`: Provides allocation methods
- `get_start_time()`, `get_end_time()`, `is_allocated()`: Standard interface

### 3. Evaluation Metrics
```python
eval_dict = problem.evaluate(solution)
# Returns:
# {
#     "cycle_time": float,           # Objective to minimize
#     "penalty_precedence": float,   # Precedence violations
#     "penalty_resource": float,     # Resource over-consumption
#     "penalty_unscheduled": float,  # Tasks without valid schedule
# }
```

## Exercise: CP-SAT Solver

The `exercises.py` file provides a skeleton for implementing a CP-SAT solver. You need to complete **7 TODOs**:

### TODO 1.1: Task Assignment Variables
Create integer variables to assign each task to a station.

### TODO 1.2: Start Time and Interval Variables
Create temporal variables for scheduling tasks within stations.

### TODO 1.3: Station Precedence Constraints
Ensure tasks flow forward through the assembly line (predecessor stations must come before successor stations).

### TODO 1.4: Temporal Precedence (Same Station)
If two tasks are on the same station AND have a precedence relation, enforce temporal ordering between them.

**Challenge**: How to make this constraint conditional on tasks being on the same station?

### TODO 1.5: Resource Constraints (Key Challenge)
Add cumulative constraints **per station**.

**Main Challenge**: In CP-SAT, how can you apply a constraint to only the tasks assigned to a specific station, when task assignment itself is a decision variable?

**Hint**: Review Lesson 2 on advanced CP-SAT techniques.

### TODO 1.6: Objective Function
Define the optimization objective (what are we trying to minimize?).

### TODO 1.7: Extract Solution
Convert CP-SAT variable values into a `RCALBPSolution` object.

## Learning Objectives

By completing this TP, you will:

1. **Understand** resource-constrained scheduling problems
2. **Model** scheduling problems with the discrete-optimization framework
3. **Implement** CP-SAT solver with optional intervals (advanced technique!)
4. **Use** conditional constraints with `OnlyEnforceIf`
5. **Handle** two types of precedence constraints
6. **Analyze** trade-offs between solution quality and computation time

## Connections to Course Content

### From Lesson 1 (RCPSP)
- Serial Generation Scheme (SGS) heuristic
- Priority rules for task ordering
- Critical path analysis

### From Lesson 2 (CP-SAT + Job Shop)
- Interval variables for scheduling
- `AddCumulative` constraint for resources (allows overlaps!)
- Optional intervals (new technique for this TP)
- Precedence constraints

### From TP1 (RCPSP Practical)
- Using `discrete-optimization` library
- Benchmarking methodology
- Solution validation

## Differences from RCPSP

| Aspect | RCPSP | RC-ALBP (this TP) |
|--------|-------|-------------------|
| **Stations** | Not fixed | Fixed number |
| **Objective** | Minimize makespan | Minimize cycle time |
| **Resources** | Renewable, global | Allocated per station |
| **Focus** | Project scheduling | Line balancing |

## Realistic Instances from RCPSP

The `utils.py` module now includes functions to create **realistic** RC-ALBP instances from RCPSP problems:

### How it Works

```python
from scheduling.tp2_assembly_line_balancing.utils import load_rcpsp_as_albp

# Load RCPSP instance j301_1 (30 tasks, 4 resources)
# Convert to RC-ALBP with 3 stations
problem = load_rcpsp_as_albp('j301_1', nb_stations=3)

# Result:
# - Tasks: Same as RCPSP (with precedences, durations)
# - Resources: RCPSP global capacity split across stations
# - Consumption: Same as RCPSP
```

### Conversion Process

1. **Tasks**: Use RCPSP task durations
2. **Precedences**: Use RCPSP precedence graph
3. **Resources**: Split RCPSP global capacity across stations
   - Base allocation: divide equally
   - Add variation (+/- 20%)
   - Ensure total ≤ original capacity
4. **Consumption**: Use RCPSP resource consumption per task

### Available Instances

From PSPLib:
- `j301_X`: 30 tasks, 4 resources
- `j601_X`: 60 tasks, 4 resources
- `j1201_X`: 120 tasks, 4 resources

### Benchmarking

The `benchmark.py` script:
1. Loads multiple RCPSP instances
2. Converts to RC-ALBP with different station counts
3. Solves with CP-SAT
4. Stores results in DataFrame (CSV)
5. Analyzes performance statistics

**Output**: `tp2_benchmark_results.csv` with columns:
- `instance`, `nb_stations`, `nb_tasks`, `nb_resources`
- `cycle_time`, `solve_time`, `gap_percent`
- `is_valid`, `is_optimal`, `status`

## Expected Outputs

### Solver Implementation (exercises.py)

**Code Requirements:**
- Complete implementation of `RCALBPCpSatSolver` class
- All 7 TODOs completed with working code
- Solutions must pass `problem.satisfy(solution)` validation check

**Documentation Requirements:**
Your code should include comments explaining:

**1. Variable Roles:**
- Task assignment variables (what do they represent?)
- Start time and interval variables (temporal decisions)
- Optional interval variables (why optional? when are they active?)

**2. Constraint Types:**
- **Station precedence**: Purpose and formulation
- **Temporal precedence**: When does it apply? How is it made conditional?
- **Resource constraints per station**: The key challenge of this TP
  - Why can't we use simple cumulative constraints like in RCPSP?
  - How do optional intervals solve the problem?
  - How are tasks filtered by station in the CP model?

**3. Key Modeling Differences:**
Explain how RC-ALBP differs from:
- **RCPSP**: Fixed stations vs global resources
- **Job Shop**: Multiple precedence types, resource allocation per station

**Testing:**
- Run on tutorial example (verify manually)
- Test on at least one realistic instance (e.g., `load_rcpsp_as_albp('j301_1', nb_stations=3)`)
- Verify with `problem.satisfy(solution) == True`
- Use interactive visualization to validate task assignments and resource usage

### Benchmark Analysis (benchmark.py)

**Output Files:**
- `tp2_benchmark_results.csv`: Raw experimental data
- `benchmark_results_*.png`: Performance analysis plots
- Interactive flow visualization demonstrating solution quality

**Written Analysis:**
Provide detailed insights on:

**1. Cycle Time vs Number of Stations:**
- How does cycle time change as you add more stations?
- Is there a point of diminishing returns?
- Explain the relationship between station count and cycle time

**2. Solver Performance:**
- Computation time trends across different configurations
- Which instances are hardest to solve? Why?
- Optimality rates: how often does CP-SAT prove optimality?

**3. Resource Utilization:**
- Using the interactive visualization, identify bottleneck stations
- Measure idle time and balancing loss
- Which stations are underutilized?

**4. Practical Recommendations:**
For a real assembly line manager, recommend:
- Optimal number of stations for given instance
- Trade-offs between cycle time and number of stations (cost vs throughput)
- How to identify and address resource bottlenecks

## Extensions for Realism

Want to make this problem more realistic? Consider these extensions:

### 1. Learning Effects
Workers become faster at repetitive tasks. Model task duration reduction at later stations:
```python
effective_duration = base_duration * (0.95 ** station_index)
```

### 2. Worker Skills and Specialization
Not all workers can perform all tasks. Add skill requirements:
- Tasks require specific skills (welding, assembly, testing)
- Stations have workers with different skill sets
- Constraint: Task can only be assigned to station with required skills

### 3. Setup Times
Time required to switch between different task types:
- If Task A (type: metal) followed by Task B (type: electrical), add setup time
- Model with additional interval variables for setups

### 4. Multi-Product Assembly Lines
Handle multiple product variants on the same line:
- Different products have different task sequences
- Some tasks are common, some are product-specific
- Constraint: Station must handle tasks from all products passing through

### 5. Quality Gates
Certain critical tasks (e.g., safety testing) must be performed at specific stations:
- Fixed assignment constraints for quality-critical tasks
- Resource requirements for inspection equipment

### 6. Balancing Loss Metrics
Quantify inefficiency:
```python
balancing_loss = (cycle_time * nb_stations - sum(task_times)) / (cycle_time * nb_stations)
smoothness_index = std_dev(station_workloads) / mean(station_workloads)
```

### 7. Precedence Relaxation
Some precedence constraints could be relaxed if tasks are independent:
- Identify "soft" vs "hard" precedences
- Allow parallel execution of independent sub-assemblies

These extensions provide opportunities for more advanced projects or research directions.

## Next Steps

1. **Run the tutorial**: `uv run python -m scheduling.tp2_assembly_line_balancing.tutorial`
2. **Study the problem class**: Understand the data structures
3. **Implement the solver**: Complete the 7 TODOs in `exercises.py`
4. **Test on realistic instances**: Use `load_rcpsp_as_albp()`
5. **Run benchmarks**: Analyze performance with `benchmark.py`
6. **Analyze results**: Load CSV in pandas/Jupyter for visualization

## References

- **SALBP**: Simple Assembly Line Balancing Problem
- **RCALBP/L**: Resource-Constrained Assembly Line Balancing with Learning
- **discrete-optimization**: https://github.com/airbus/discrete-optimization

---

