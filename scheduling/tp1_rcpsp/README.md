# TP1: Resource-Constrained Project Scheduling Problem (RCPSP)

## Overview

This practical work (TP) applies the concepts from Lessons 1 and 2 to the **Resource-Constrained Project Scheduling Problem (RCPSP)**. You will implement a complete CP-SAT solver and compare it against heuristic approaches.

### What is RCPSP?
See Lesson 1 :-).

## Learning Objectives

By completing this TP, you will:

1. **Model** RCPSP using CP-SAT constraints
2. **Implement** a complete CP-SAT solver using the discrete-optimization framework
3. **Compare** heuristic vs exact approaches through systematic benchmarking
4. **Analyze** trade-offs between solution quality and computation time

## The RCPSP Problem

### Problem Definition

<table border="1">
<tr bgcolor="#e6f7ff">
  <th style="color:black"><b>Given</b></th>
  <th style="color:black"><b>Find</b></th>
  <th style="color:black"><b>Minimize</b></th>
</tr>
<tr>
  <td>
    • Set of tasks with durations<br>
    • Precedence constraints (task graph)<br>
    • Renewable resources with capacities<br>
    • Resource consumption per task
  </td>
  <td>
    • Start time for each task<br>
    • Task execution schedule
  </td>
  <td>
    • Project makespan<br>
    (completion time)
  </td>
</tr>
</table>

### Constraints

<table border="1">
<tr bgcolor="#fff7e6">
  <th style="color:black"><b>Type</b></th>
  <th style="color:black"><b>Description</b></th>
</tr>
<tr>
  <td><b>1. Precedence</b></td>
  <td>If task A → task B in precedence graph, then: end[A] ≤ start[B]</td>
</tr>
<tr>
  <td><b>2. Resource Capacity</b></td>
  <td>
    At any time t, sum of resource consumption by active tasks ≤ resource capacity
  </td>
</tr>
</table>

### Example: Small Project

**Tasks:**
- Task 1: Duration 3, needs 2 workers
- Task 2: Duration 2, needs 1 worker
- Task 3: Duration 4, needs 2 workers
- Task 4: Duration 1, needs 1 worker

**Precedences:** 1→3, 2→4

**Resources:** 3 workers available

**Question:** Can Task 1 and Task 2 run in parallel?
- At t=0: Task 1 (2W) + Task 2 (1W) = 3W ≤ 3W capacity → **Yes!**

**Makespan:** With optimal scheduling considering precedences and resource constraints.

## TP Structure

### Part 1: CP-SAT Solver Implementation
**File:** `exercises_part1.py`

Implement a complete CP-SAT solver for RCPSP using the `discrete-optimization` framework.

**What you'll build:**
- Decision variables (start times, intervals)
- Precedence constraints
- Resource capacity constraints
- Objective function (minimize makespan)
- Solution extraction from CP-SAT solver

### Part 2: Benchmarking and Comparison Study
**File:** `exercises_part2.py`

Compare different solving approaches on multiple instances:
- **Heuristics:** SGS with different priority rules
- **Exact:** CP-SAT solver
- **Analysis:** Quality vs computation time trade-offs

**Deliverables:**
- Benchmark results on multiple instances (j30, j60, j120)
- Visualization comparing approaches
- Head-to-head comparison matrix
- CSV export of results


## Files

### Core Files
- **`exercises_part1.py`**: CP-SAT solver implementation (complete the TODOs)
- **`exercises_part2.py`**: Benchmarking study (complete the TODOs)
- **`utils.py`**: Helper functions (instance loading, validation, visualization)

### Data
RCPSP instances are loaded from **PSPLib** via the `discrete-optimization` library:
- `j301_X`: 30 tasks, 4 resources (quick testing)
- `j601_X`: 60 tasks, 4 resources (realistic evaluation)
- `j1201_X`: 120 tasks, 4 resources (challenging instances)

## How to Run

```bash
# From the repo root (aibt_108/)

# 1. Part 1: Implement and test CP-SAT solver
uv run python -m scheduling.tp1_rcpsp.exercises_part1
# 2. Part 2: Run benchmark study
uv run python -m scheduling.tp1_rcpsp.exercises_part2
```


## Exercise Structure

### Part 1: CP-SAT Solver (exercises_part1.py)

Complete the TODOs to build your solver:

**TODO 1:** Create decision variables (start times, intervals)
**TODO 2:** Add precedence constraints
**TODO 3:** Add resource capacity constraints
**TODO 4:** Define objective function
**TODO 5:** Extract and return solution

### Part 2: Benchmarking Study (exercises_part2.py)

Complete the benchmarking framework:

**TODO 1:** Configure benchmark instances and solvers
**TODO 2:** Run experiments with time limits
**TODO 3:** Generate comparison plots
**TODO 4:** Create head-to-head comparison matrix

**Analysis Focus:** Compare CP-SAT exact solver against SGS heuristics in terms of:
- Solution quality (makespan)
- Computation time
- Success rate (finding feasible solutions)

## Test Instances

<table border="1">
<tr>
  <th>Instance Family</th>
  <th>Size</th>
  <th>Typical Solve Time</th>
  <th>Use For</th>
</tr>
<tr>
  <td><b>j301_X</b></td>
  <td>30 tasks, 4 resources</td>
  <td>< 10 seconds</td>
  <td>Development, debugging</td>
</tr>
<tr>
  <td><b>j601_X</b></td>
  <td>60 tasks, 4 resources</td>
  <td>< 60 seconds</td>
  <td>Realistic evaluation</td>
</tr>
<tr>
  <td><b>j1201_X</b></td>
  <td>120 tasks, 4 resources</td>
  <td>> ? </td>
  <td>Scalability testing</td>
</tr>
</table>

**Note:** Instances are automatically downloaded from PSPLib via `discrete-optimization` on first use.

## Connections to Course Content

### From Lesson 1 (RCPSP Introduction)
- Serial Generation Scheme (SGS) heuristic
- Priority rules for task ordering
- Resource feasibility checking

### From Lesson 2 (CP-SAT + Job Shop)
- Interval variables for scheduling
- Precedence constraints
- Solution extraction from CP-SAT
- Using `discrete-optimization` framework

### New in This TP
- Benchmarking methodology
- Systematic comparison of exact vs heuristic approaches
- Performance analysis (quality vs computation time)

## Expected Outputs

### Part 1: Working CP-SAT Solver

**Code Requirements:**
- Complete implementation of `RcpspCpSatSolver` class
- All TODOs completed with working code
- Solutions must pass `problem.satisfy(solution)` validation check

**Documentation Requirements:**
Your code should include comments explaining:
- **Variable roles**: What each decision variable represents (starts, ends, intervals)
- **Constraint types**: Purpose of each constraint added to the model
  - Precedence constraints
  - Resource capacity constraints
  - Objective function
- **Key modeling choice**: How RCPSP differs from Job Shop in terms of resource constraints

**Testing:**
- Run your solver on at least 3 instances (j301_1, j301_2, j301_3)
- Verify solutions with `problem.satisfy(solution) == True`
- Compare your results with reference implementation

### Part 2: Benchmark Results

**Output Files:**
- `tp1_benchmark_results.csv`: Raw data for all experiments
- `benchmark_results_main.png`: Performance plots showing:
  - Makespan comparison across solvers
  - Computation time per instance
  - Optimality gap analysis
- `benchmark_results_h2h.png`: Head-to-head comparison matrix

**Written Analysis:**
Provide a detailed overview of solver performance including:
- **Quality comparison**: Which solver produces better solutions? By how much?
- **Speed comparison**: Computation time differences across instance sizes
- **Scalability**: How does performance change with instance size (j30 vs j60 vs j120)?

**Recommendations:**
Based on your results, provide recommendations on:
- When to use CP-SAT exact solver vs heuristics
- Which SGS priority rule performs best
- Trade-offs between solution quality and computation time
- Suggested approach for real-world scenarios (small projects vs large projects)

## References

- **PSPLib**: [http://www.om-db.wi.tum.de/psplib/](http://www.om-db.wi.tum.de/psplib/)
- **OR-Tools Documentation**: [Scheduling with OR-Tools](https://developers.google.com/optimization/scheduling)
- **discrete-optimization**: [GitHub Repository](https://github.com/airbus/discrete-optimization)

---
