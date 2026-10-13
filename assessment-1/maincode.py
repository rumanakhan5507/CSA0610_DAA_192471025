"""ShopSphere scalability audit — Assessment 1.

Uses the formulas and assumptions described in the accompanying report.
Running this file prints verification values and writes results.csv.
"""

import csv
import math
from pathlib import Path

RATE = 10
WINDOW_SECONDS = 600
MAX_OPERATIONS = RATE * WINDOW_SECONDS
OUTPUT_FILE = Path(__file__).with_name("results.csv")


def m1(n):
    """M1: all-pairs duplicate comparisons."""
    return n * (n - 1) // 2


def m2(n):
    """M2: audits for i = 1, 2, 4, ... while i < n."""
    i = 1
    count = 0
    outer_passes = 0
    while i < n:
        count += i
        outer_passes += 1
        i *= 2
    return count, outer_passes


def s2(n):
    """S2: worst-case binary-search comparisons."""
    if n < 1:
        raise ValueError("n must be at least 1")
    return math.floor(math.log2(n)) + 1


def m4_current(n):
    """M4 current recurrence closed form, as used in the report."""
    return 2 * n**2 - n


def m4_redesigned(n):
    """M4 redesigned recurrence formula used in the report."""
    return n * math.log2(n) + n


def m5(n):
    """M5 recurrence formula used in the report."""
    log_n = math.log2(n)
    return n * log_n * (log_n + 1) / 2 + n


def report_generator(n):
    """Quadratic report-generator operation-count function."""
    return 3 * n**2 + 10 * n * math.log2(n) + 50


def s1_average(n, success_probability=0.5):
    """Average comparisons for sequential search under the report's model."""
    return success_probability * ((n + 1) / 2) + (1 - success_probability) * n


def write_results():
    n = 1_000_000
    modules = [
        ("M1 - Duplicate detector", m1(n), "Theta(n^2)"),
        ("M2 - API rate limiter", m2(n)[0], "Theta(n)"),
        ("S2 - Binary search", s2(n), "Theta(log n)"),
        ("M4 - Current design", m4_current(n), "Theta(n^2)"),
        ("M4 - Redesigned", m4_redesigned(n), "Theta(n log n)"),
        ("M5 - Sales analytics", m5(n), "Theta(n log^2 n)"),
        ("Report generator", report_generator(n), "Theta(n^2)"),
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Module",
            "Input Size (n)",
            "Operation Count",
            "Estimated Time (seconds at 10 ops/s)",
            "Within 10-Minute Window",
            "Time Complexity",
        ])
        for name, operations, complexity in modules:
            runtime = operations / RATE
            writer.writerow([
                name,
                n,
                f"{operations:.2f}",
                f"{runtime:.2f}",
                "Yes" if runtime <= WINDOW_SECONDS else "No",
                complexity,
            ])


def print_verification():
    print("=== M1: Duplicate comparisons ===")
    for n in (1_000, 100_000, 1_000_000):
        print(f"n = {n:,} | Comparisons = {m1(n):,}")

    print("\\n=== M2: API rate limiter ===")
    for n in (1_024, 100_000, 1_000_000):
        audits, passes = m2(n)
        print(f"n = {n:,} | Audits = {audits:,} | Outer passes = {passes}")

    print("\\n=== S2 and recurrence formulas ===")
    n = 1_024
    print(f"n = {n:,}")
    print(f"S2 worst-case comparisons = {s2(n):,}")
    print(f"M4 current formula = {m4_current(n):,.0f}")
    print(f"M4 redesigned formula = {m4_redesigned(n):,.0f}")
    print(f"M5 formula = {m5(n):,.0f}")

    n = 1_000_000
    print(f"\\nAt n = {n:,}:")
    print(f"S1 average comparisons (p=0.5) = {s1_average(n):,.2f}")
    print(f"S2 worst-case comparisons = {s2(n):,}")

    print("\\n=== Report generator bound checks ===")
    for n in (1, 10, 100, 1_000, 1_000_000):
        value = report_generator(n)
        lower = 3 * n**2
        upper = 63 * n**2
        print(
            f"n={n:,} | f(n)={value:,.2f} | "
            f"3n^2={lower:,} | 63n^2={upper:,} | "
            f"Bound holds: {lower <= value <= upper}"
        )

    print("\\n=== Scalability assumptions ===")
    print(f"Server rate: {RATE} operations/second")
    print(f"Processing window: {WINDOW_SECONDS} seconds")
    print(f"Maximum allowed operations: {MAX_OPERATIONS:,}")


if __name__ == "__main__":
    print_verification()
    write_results()
    print(f"\\nScalability results written to: {OUTPUT_FILE}")
