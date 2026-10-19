# Design and Analysis of Algorithms — Assignment 2

This project contains Python 3 implementations and small experiments for Questions 1–7 from the assignment report.

## Files

- `maincode.py` — all algorithm implementations and experiment driver.
- `README.md` — setup and run instructions.

## Requirements

- Python 3.9 or newer (Python 3.8+ should also work).
- No third-party packages are required.

## How to run

Open a terminal in the folder containing `maincode.py`, then run:

```bash
python maincode.py
```

On some systems, use:

```bash
python3 maincode.py
```

The program prints experiment results and operation counts to the terminal. Runtime measurements vary by computer and Python version, so use the values printed by your own run when reporting local timings.

## Included questions

1. **Sorting:** Selection Sort, Bubble Sort, and Insertion Sort on nearly sorted, reverse-order, and already-sorted inputs.
2. **Sequential Search:** comparison counts for first, middle, last, and missing targets at multiple input sizes.
3. **Brute-force string matching:** match positions and character-comparison counts for several text/pattern cases.
4. **Closest pair:** checks every unique pair of 2D points and reports the closest pair, distance, and number of distance calculations.
5. **Convex hull:** tests candidate supporting lines and returns the hull vertices in boundary order.
6. **Exhaustive knapsack:** checks every subset and reports the best feasible selection, weight, value, and subset counts.
7. **Redesign and validation:** compares brute-force string matching with Knuth–Morris–Pratt (KMP), which reuses prefix information to reduce repeated comparisons.

## Notes

- String match positions are zero-based.
- The closest-pair implementation compares squared distances to avoid square roots inside the pair loop.
- The convex-hull implementation uses a brute-force supporting-line check for the experiment and a monotonic-chain step to order the boundary vertices for output.
- Exhaustive knapsack is exponential in the number of items; keep larger tests modest.
- These are educational implementations intended to reproduce the assignment experiments, not production-grade optimized systems.
