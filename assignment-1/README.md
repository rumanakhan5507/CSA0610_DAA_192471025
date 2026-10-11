# Design and Analysis of Algorithms – Assignment 1

**Student:** M. Rumana Khan  
**Register Number:** 192471025  
**Course:** CSA0610 – Design and Analysis of Algorithms  
**Assignment:** Design, Analyse and Validate an Efficient Search Strategy for a Large-Scale Student Record System

## Files included
1. `algorithms_used.py` – standalone implementations of the three search algorithms and their comparison counters.
2. `main_code.py` – complete experiment program corresponding to the assignment appendix. It generates datasets, tests the algorithms, times searches and preprocessing, validates correctness, and prints the results.
3. `results.csv` – experimental values reported in the assignment, plus best/average/worst theoretical comparison counts for the dataset sizes.
4. `comparisons plot.png` – The plot compares the number of key comparisons required by linear search, binary search, and hash tables as database size increases.

## Algorithms used
- **Linear Search:** Iterative brute-force search; no preprocessing; best Θ(1), average Θ(n), worst Θ(n).
- **Recursive Binary Search:** Decrease-and-conquer; requires sorted data; best Θ(1), average Θ(log n), worst Θ(log n).
- **Hash Table Search with Chaining:** Transform-and-conquer; expected Θ(1) average search with a controlled load factor, but Θ(n) worst case if many keys collide.

## Requirements
- Python 3.8 or later
- No third-party packages are required.

## Run
Open a terminal in this folder and run:

```bash
python main_code.py
```

The program prints the measured comparison counts and elapsed times. Exact timings can vary by computer and Python version.

## Notes on interpreting results
- The assignment's reported experiment used `n = 1,000`, `10,000`, `100,000`, and `1,000,000`.
- It used 1,000 queries per size (500 present and 500 absent), except linear search at `n = 1,000,000`, which used 100 queries to reduce runtime.
- The reported measurements are copied from the submitted assignment. `main_code.py` is an executable reproduction of the experiment design; machine timings may differ.
- For linear search, the assignment's mixed-query average prediction is approximately `0.75n` comparisons (half successful searches with average position near `n/2`, and half unsuccessful searches requiring `n` comparisons).
- Binary search's exact average depends on the searched keys and the mix of successful and unsuccessful queries. The asymptotic average is Θ(log n).
- Hash search has expected Θ(1) search cost under reasonably uniform hashing and a bounded load factor; its worst case is Θ(n).
