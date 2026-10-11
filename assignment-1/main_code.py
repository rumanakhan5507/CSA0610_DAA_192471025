"""Main experiment program for DAA Assignment 1.

Runs linear search, recursive binary search, and hash-table search for
n = 1,000, 10,000, 100,000, and 1,000,000. Timings vary by machine.
"""

import random
import time
from algorithms_used import (
    linear_search,
    binary_search_recursive,
    HashTableChaining,
)


def timed_ms(function):
    start = time.perf_counter()
    result = function()
    elapsed_ms = (time.perf_counter() - start) * 1000
    return result, elapsed_ms


def run_experiments():
    random.seed(42)
    query_count = 1000
    sizes = [1000, 10000, 100000, 1000000]

    print(
        "n,linear_avg_ms,linear_avg_comparisons,"
        "binary_avg_ms,binary_avg_comparisons,"
        "hash_avg_ms,hash_avg_comparisons,sort_ms,hash_build_ms"
    )

    for n in sizes:
        # Generate unique registration-number-like integer keys.
        data = random.sample(range(20200000, 20200000 + n * 20), n)
        present = random.sample(data, query_count // 2)
        absent = [
            20200000 + n * 20 + i for i in range(query_count // 2)
        ]
        queries = present + absent
        random.shuffle(queries)

        sorted_data, sort_ms = timed_ms(lambda: sorted(data))

        def build_hash():
            table = HashTableChaining(n)
            for key in data:
                table.add(key)
            return table

        hash_table, hash_build_ms = timed_ms(build_hash)

        # The assignment used 100 linear queries for n = 1,000,000.
        linear_queries = queries if n <= 100000 else queries[:100]

        def run_linear():
            comparison_total = 0
            for query in linear_queries:
                _, comparisons = linear_search(data, query)
                comparison_total += comparisons
            return comparison_total

        linear_total, linear_ms_total = timed_ms(run_linear)
        linear_avg_ms = linear_ms_total / len(linear_queries)
        linear_avg_comparisons = linear_total / len(linear_queries)

        def run_binary():
            comparison_total = 0
            for query in queries:
                counter = [0]
                binary_search_recursive(
                    sorted_data, query, 0, n - 1, counter
                )
                comparison_total += counter[0]
            return comparison_total

        binary_total, binary_ms_total = timed_ms(run_binary)
        binary_avg_ms = binary_ms_total / query_count
        binary_avg_comparisons = binary_total / query_count

        def run_hash():
            comparison_total = 0
            for query in queries:
                _, comparisons = hash_table.find(query)
                comparison_total += comparisons
            return comparison_total

        hash_total, hash_ms_total = timed_ms(run_hash)
        hash_avg_ms = hash_ms_total / query_count
        hash_avg_comparisons = hash_total / query_count

        # Correctness validation against Python set membership.
        reference = set(data)
        for query in queries[:200]:
            linear_found, _ = linear_search(data, query)
            binary_found = binary_search_recursive(
                sorted_data, query, 0, n - 1, [0]
            )
            hash_found, _ = hash_table.find(query)
            assert linear_found == binary_found == hash_found == (query in reference)

        print(
            f"{n},{linear_avg_ms:.6f},{linear_avg_comparisons:.2f},"
            f"{binary_avg_ms:.6f},{binary_avg_comparisons:.2f},"
            f"{hash_avg_ms:.6f},{hash_avg_comparisons:.2f},"
            f"{sort_ms:.3f},{hash_build_ms:.3f}"
        )


if __name__ == "__main__":
    run_experiments()
