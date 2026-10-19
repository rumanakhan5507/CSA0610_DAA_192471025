"""DAA Assignment 2: implementations and experiments for Q1-Q7."""
import math
import time


def sorting_algorithm(values, method):
    a = values[:]
    comparisons = swaps = moves = 0
    n = len(a)
    if method == "selection":
        for i in range(n - 1):
            minimum = i
            for j in range(i + 1, n):
                comparisons += 1
                if a[j] < a[minimum]:
                    minimum = j
            if minimum != i:
                a[i], a[minimum] = a[minimum], a[i]
                swaps += 1
                moves += 3
    elif method == "bubble":
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                comparisons += 1
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swaps += 1
                    moves += 3
                    swapped = True
            if not swapped:
                break
    elif method == "insertion":
        for i in range(1, n):
            key = a[i]
            j = i - 1
            while j >= 0:
                comparisons += 1
                if a[j] > key:
                    a[j + 1] = a[j]
                    moves += 1
                    j -= 1
                else:
                    break
            a[j + 1] = key
            moves += 1
    else:
        raise ValueError("Unknown sorting method")
    return a, comparisons, swaps, moves


def sequential_search(records, target):
    comparisons = 0
    for index, value in enumerate(records):
        comparisons += 1
        if value == target:
            return index, comparisons
    return -1, comparisons


def brute_force_string_match(text, pattern):
    comparisons = 0
    matches = []
    if pattern == "":
        return list(range(len(text) + 1)), comparisons
    for start in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern):
            comparisons += 1
            if text[start + j] != pattern[j]:
                break
            j += 1
        if j == len(pattern):
            matches.append(start)
    return matches, comparisons


def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    comparisons = 0
    while i < len(pattern):
        comparisons += 1
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps, comparisons


def kmp_search(text, pattern):
    if pattern == "":
        return list(range(len(text) + 1)), 0
    lps, comparisons = build_lps(pattern)
    matches = []
    i = j = 0
    while i < len(text):
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                matches.append(i - j)
                j = lps[j - 1]
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return matches, comparisons


def closest_pair(points):
    best_squared = float("inf")
    best_pair = None
    distance_calculations = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance_calculations += 1
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            squared = dx * dx + dy * dy
            if squared < best_squared:
                best_squared = squared
                best_pair = (points[i], points[j])
    distance = math.sqrt(best_squared) if best_pair else None
    return best_pair, distance, distance_calculations


def cross(o, a, b):
    return ((a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0]))


def convex_hull(points):
    """Brute-force supporting-line tests; monotonic chain orders hull vertices."""
    pts = sorted(set(points))
    n = len(pts)
    side_tests = 0
    if n <= 1:
        return pts, side_tests

    candidate_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            positive = negative = False
            for k in range(n):
                if k == i or k == j:
                    continue
                side_tests += 1
                value = cross(pts[i], pts[j], pts[k])
                if value > 0:
                    positive = True
                elif value < 0:
                    negative = True
                if positive and negative:
                    break
            if not (positive and negative):
                candidate_edges.append((pts[i], pts[j]))

    # Return consistently ordered boundary vertices for display.
    lower = []
    for point in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    ordered_hull = lower[:-1] + upper[:-1]
    return ordered_hull, side_tests


def exhaustive_knapsack(weights, values, capacity):
    n = len(weights)
    subsets_examined = feasible_subsets = 0
    best_value = -1
    best_weight = 0
    best_mask = 0
    for mask in range(1 << n):
        subsets_examined += 1
        total_weight = total_value = 0
        for i in range(n):
            if mask & (1 << i):
                total_weight += weights[i]
                total_value += values[i]
        if total_weight <= capacity:
            feasible_subsets += 1
            if total_value > best_value:
                best_value = total_value
                best_weight = total_weight
                best_mask = mask
    selected = [i for i in range(n) if best_mask & (1 << i)]
    return selected, best_weight, best_value, subsets_examined, feasible_subsets


def main():
    print("Q1: SORTING")
    datasets = {
        "Nearly sorted": [1, 2, 3, 5, 4, 6, 7],
        "Reverse order": [7, 6, 5, 4, 3, 2, 1],
        "Already sorted": [1, 2, 3, 4, 5, 6, 7],
    }
    for label, data in datasets.items():
        for method in ("selection", "bubble", "insertion"):
            start = time.perf_counter()
            result, comps, swaps, moves = sorting_algorithm(data, method)
            elapsed = time.perf_counter() - start
            print(label, method, "sorted=", result, "comparisons=", comps,
                  "swaps=", swaps, "moves=", moves, "seconds=", elapsed)

    print("\nQ2: SEQUENTIAL SEARCH")
    for n in (10, 100, 1000):
        records = list(range(1, n + 1))
        for label, target in (("first", 1), ("middle", records[n // 2]),
                              ("last", n), ("missing", n + 1)):
            _, comps = sequential_search(records, target)
            print("n=", n, label, "comparisons=", comps)

    print("\nQ3 and Q7: STRING MATCHING")
    tests = [
        ("low-work", "SYSTEM ALERT: disk online", "ALERT"),
        ("repeated-prefix", "a" * 40 + "b", "a" * 19 + "c"),
        ("match-near-end", "header......LOGIN_SUCCESS", "LOGIN_SUCCESS"),
    ]
    for label, text, pattern in tests:
        matches, comps = brute_force_string_match(text, pattern)
        print(label, "matches=", matches, "comparisons=", comps)

    text = "a" * 1000 + "b"
    pattern = "a" * 40 + "b"
    start = time.perf_counter()
    brute_matches, brute_comps = brute_force_string_match(text, pattern)
    brute_time = time.perf_counter() - start
    start = time.perf_counter()
    kmp_matches, kmp_comps = kmp_search(text, pattern)
    kmp_time = time.perf_counter() - start
    print("Q7 brute force:", brute_matches, brute_comps, brute_time)
    print("Q7 prefix reuse:", kmp_matches, kmp_comps, kmp_time)

    print("\nQ4: CLOSEST PAIR")
    for n in (10, 100, 1000):
        points = [(i, (i * 37) % 101) for i in range(n)]
        start = time.perf_counter()
        pair, distance, count = closest_pair(points)
        elapsed = time.perf_counter() - start
        print("n=", n, "pairs=", count, "distance_calculations=", count,
              "closest_pair=", pair, "distance=", distance, "seconds=", elapsed)

    print("\nQ5: CONVEX HULL")
    point_sets = [
        ("boundary_and_interior",
         [(0, 0), (4, 0), (4, 3), (0, 3), (2, 1), (1, 2), (3, 2)]),
        ("challenge",
         [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (0, 3), (0, -2), (1, 1)]),
    ]
    for label, points in point_sets:
        hull, tests = convex_hull(points)
        print(label, "hull=", hull, "side_tests=", tests)

    print("\nQ6: EXHAUSTIVE KNAPSACK")
    items = [("P1", 2, 6), ("P2", 3, 8), ("P3", 4, 9), ("P4", 5, 10)]
    weights = [item[1] for item in items]
    values = [item[2] for item in items]
    chosen, weight, value, examined, feasible = exhaustive_knapsack(weights, values, 7)
    print("small instance selected=", [items[i][0] for i in chosen],
          "weight=", weight, "value=", value,
          "subsets_examined=", examined, "feasible=", feasible)
    for n in (4, 10, 15, 20):
        weights = [(i % 5) + 1 for i in range(n)]
        values = [((i * 7) % 13) + 3 for i in range(n)]
        _, _, _, examined, feasible = exhaustive_knapsack(
            weights, values, max(5, n * 2))
        print("n=", n, "subsets=", examined, "feasible=", feasible)


if __name__ == "__main__":
    main()
