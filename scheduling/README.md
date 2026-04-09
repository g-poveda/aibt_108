# Scheduling Problems - Practical Course

Learn to model and solve scheduling problems using heuristics and Constraint Programming (OR-Tools CP-SAT).

## Course Structure

**Duration:** 1 day (8 hours)
- 1 hour: Course slides (scheduling fundamentals)
- 1.5 hours: Lesson 1 (RCPSP + heuristics)
- 1.5 hours: Lesson 2 (CP-SAT + Job Shop)
- 2 hours: TP1 (graded)
- 2 hours: TP2 (graded)

## Installation

Using `uv` (recommended):
```bash
uv sync
```

Using pip:
```bash
pip install discrete-optimization matplotlib numpy pandas
```

## Learning Path

Follow modules in order:

```
Lesson 1: RCPSP + Heuristics  →  TP1: RCPSP with CP-SAT (graded)
           ↓                            ↓
Lesson 2: CP-SAT + Job Shop   →  TP2: Assembly Line Balancing (graded)
```

---

## Lesson 1: RCPSP Heuristics

**Location:** `lesson1_rcpsp/`

```bash
uv run python -m scheduling.lesson1_rcpsp.tutorial
uv run python -m scheduling.lesson1_rcpsp.exercises
```

---

## Lesson 2: CP-SAT + Job Shop

**Location:** `lesson2_cpsat/`

```bash
uv run python -m scheduling.lesson2_cpsat.solutions
```

---

## TP1: RCPSP with CP-SAT (GRADED)

**Location:** `tp1_rcpsp/`

See `tp1_rcpsp/README.md` for detailed instructions.

```bash
uv run python -m scheduling.tp1_rcpsp.exercises_part1  # Part 1: Implement solver
uv run python -m scheduling.tp1_rcpsp.exercises_part2  # Part 2: Benchmark
```

---

## TP2: Assembly Line Balancing (GRADED)

**Location:** `tp2_assembly_line_balancing/`

See `tp2_assembly_line_balancing/README.md` for detailed instructions.

```bash
uv run python -m scheduling.tp2_assembly_line_balancing.tutorial
uv run python -m scheduling.tp2_assembly_line_balancing.exercises
uv run python -m scheduling.tp2_assembly_line_balancing.benchmark
```

---

## Resources

- **discrete-optimization:** https://airbus.github.io/discrete-optimization/
- **OR-Tools CP-SAT:** https://developers.google.com/optimization/cp
- **Module READMEs:** See each folder for detailed instructions

For questions: Open an issue or contact g-poveda