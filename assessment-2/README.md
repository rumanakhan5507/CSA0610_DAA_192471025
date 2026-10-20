# DAA Assessment 2 – SentinelOps Alert-Triage Module

## Student Details

- **Name:** M. Rumana Khan
- **Register Number:** 192471025
- **Course Code:** CSA0610
- **Course Name:** Design and Analysis of Algorithms
- **Assignment:** Assessment 2 – Debugging & Optimisation of the SentinelOps SOC Alert-Triage Module

## Project Overview

This assignment focuses on identifying, correcting, testing, and optimising defects in a Python-based Security Operations Centre (SOC) alert-triage module called **SentinelOps**.

The module handles four main tasks:

1. Sorting security alerts by severity in descending order while preserving the arrival order of alerts with equal severity.
2. Checking source IP addresses against a blocklist.
3. Finding all occurrences of an attack signature in a log string.
4. Finding the closest pair of login locations.

## Project Files

- `sentinelops.py` – Corrected and optimised implementation of the SentinelOps functions.
- `test_sentinelops.py` – Unit tests for the module, including sample inputs, boundary cases, and comparisons with reference implementations.
- `analysis.py` – Script used to measure operation counts and execution times for the algorithm analysis.

Make sure these files are placed in the repository if you intend to run the commands below.

## Requirements

- Python 3
- No third-party packages are required; the code uses Python standard-library modules.

To check your Python version, run:

```bash
python --version
```

## How to Run

### 1. Run the SentinelOps module

```bash
python sentinelops.py
```

### 2. Run the unit tests

```bash
python -m unittest -v test_sentinelops
```

The assignment report records **25 passing tests** for the test harness.

### 3. Run the performance analysis

```bash
python analysis.py
```

The analysis script compares operation counts and execution times for the corrected baseline algorithms and their optimised versions.

## Defects Corrected

The original implementation contained nine defects:

- Fixed insertion-sort loop boundaries and insertion position.
- Corrected the return value when an IP address is found in the blocklist.
- Included the final possible starting position during signature matching.
- Corrected match detection after character comparisons.
- Initialised the closest-pair minimum distance correctly.
- Changed the closest-pair comparison to retain the smallest distance.
- Excluded self-pairs and duplicate mirrored pairs.

## Optimisations

- Replaced the production alert sort with Python's stable built-in sort.
- Used a `frozenset` for efficient repeated blocklist lookups.
- Improved brute-force signature matching with boundary checks and early termination on mismatches.
- Optimised closest-login search by sorting on the x-coordinate, comparing squared distances, and pruning pairs that cannot improve the current best result.

## Testing and Results

The report documents 25 passing unit tests covering normal inputs, boundary cases, duplicate locations, tie handling, and random comparisons against corrected baseline implementations.

The report also records performance measurements showing that the optimised closest-login algorithm performs substantially fewer distance calculations on uniformly distributed test data. Its worst-case time complexity remains quadratic.

## Academic Integrity

This repository contains work prepared for **CSA0610 – Design and Analysis of Algorithms, Assessment 2**.

---

**Student:** M. Rumana Khan  
**Register Number:** 192471025
