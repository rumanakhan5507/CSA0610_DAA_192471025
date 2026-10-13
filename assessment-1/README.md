# ShopSphere Scalability Audit — Assessment 1

## Overview
This project checks the operation-count formulas used in the Design and Analysis of Algorithms assignment, **“Scalability Audit of an E-Commerce Platform (ShopSphere)”**.

The program covers:
- M1 — Duplicate-listing detector
- M2 — API rate limiter
- S2 — Binary search
- M4 — Recommendation engine (current and redesigned)
- M5 — Sales analytics
- Report generator — quadratic function and asymptotic-bound checks
- S1 — Average sequential-search comparisons

## Requirements
- Python 3.8 or later
- No third-party packages are required.

## How to run
1. Keep `main code.py` and `results.csv` in the same folder.
2. Open a terminal or command prompt in that folder.
3. Run:

   ```bash
   python "main code.py"
   ```

4. The program prints verification results and rewrites `results.csv` with the scalability table for `n = 1,000,000`.

## Assumptions used
- Server processing rate: 10 basic operations per second.
- Nightly processing window: 600 seconds (10 minutes).
- Maximum allowed operations: 10 × 600 = 6,000.
- Logarithms are base 2.
- The recurrence formulas used for M4 and M5 are the formulas stated in the report. Their closed-form counts are exact for the power-of-two recurrence setup; at `n = 1,000,000`, they are used as formula-based estimates as in the report.

## Complexity summary
- M1: Θ(n²)
- M2: Θ(n)
- S2: Θ(log n)
- M4 current: Θ(n²)
- M4 redesigned: Θ(n log n)
- M5: Θ(n log² n)
- Report generator: Θ(n²)

## Important interpretation
The running times are theoretical estimates calculated by dividing the operation count by 10. They are not measured execution times on a real server. Under the assignment's assumptions, only S2 stays within the 6,000-operation budget at one million records.
