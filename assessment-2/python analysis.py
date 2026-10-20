"""Part (d) measurements. Run:  python analysis.py   (under a minute)

Counts are taken with explicit counters placed on the SAME loop structure as
the functions in sentinelops.py / fixed_only.py, so they measure the real
algorithms rather than a formula.
"""
import math
import random
import time

from sentinelops import closest_logins, closest_logins_bruteforce


# ---------------- closest pair: distance computations ----------------------
def count_original_buggy(n):
    """Original code evaluates every ordered pair incl. self pairs: n*n distances."""
    return n * n


def count_bruteforce(events):
    """Corrected brute force, instrumented: one distance per unordered pair."""
    cnt = 0
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            cnt += 1
    return cnt


def count_optimised(events):
    """Optimised sweep, same loop as closest_logins, counting distance evaluations."""
    n = len(events)
    order = sorted(range(n), key=lambda k: events[k][0])
    best_sq, cnt = math.inf, 0
    for a in range(n - 1):
        xi, yi = events[order[a]]
        for b in range(a + 1, n):
            xj, yj = events[order[b]]
            dx2 = (xj - xi) ** 2
            if dx2 > best_sq:
                break
            cnt += 1
            d2 = dx2 + (yj - yi) ** 2
            if d2 < best_sq:
                best_sq = d2
    return cnt


def closest_pair_table():
    rng = random.Random(42)
    print("\n== closest_logins: distance computations (uniform random, 1000 x 1000 km) ==")
    print(f"{'events n':>9} {'original':>12} {'brute (fixed)':>14} {'optimised':>10} "
          f"{'saving':>8} {'t_brute s':>10} {'t_opt s':>8}")
    for n in (1000, 2000, 4000, 8000):
        ev = [(rng.uniform(0, 1000), rng.uniform(0, 1000)) for _ in range(n)]
        brute = count_bruteforce(ev)
        opt = count_optimised(ev)
        t0 = time.perf_counter(); r1 = closest_logins_bruteforce(ev); t1 = time.perf_counter()
        r2 = closest_logins(ev); t2 = time.perf_counter()
        assert r1 == r2, "outputs differ!"
        print(f"{n:>9} {count_original_buggy(n):>12,} {brute:>14,} {opt:>10,} "
              f"{brute / opt:>7.0f}x {t1 - t0:>10.2f} {t2 - t1:>8.3f}")
    # worst case for the pruning: every login has the same x
    n = 2000
    ev = [(500.0, rng.uniform(0, 1000)) for _ in range(n)]
    print(f"\nWorst case for pruning (all x equal, n={n}): optimised = "
          f"{count_optimised(ev):,} vs brute = {count_bruteforce(ev):,}")


# ---------------- insertion sort: comparisons ------------------------------
def insertion_comparisons(sev):
    a = list(sev)
    cmp = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            cmp += 1                      # one evaluation of a[j] < key
            if a[j] < key:
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = key
    return cmp


class Counted:
    n = 0
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        Counted.n += 1
        return self.v < other.v


def timsort_comparisons(sev):
    Counted.n = 0
    items = [Counted(v) for v in sev]
    items.sort(reverse=True)
    return Counted.n


def sort_table():
    rng = random.Random(7)
    print("\n== sort_alerts: comparisons, severity descending ==")
    print(f"{'n':>7} {'input':>14} {'insertion':>12} {'Timsort':>10} {'n^2/4':>12}")
    for n in (1000, 5000, 10000):
        rand = [rng.randint(1, 1_000_000) for _ in range(n)]
        near = sorted(rand, reverse=True)           # already in the right order ...
        for _ in range(n // 100):                    # ... then 1% adjacent swaps
            k = rng.randrange(n - 1)
            near[k], near[k + 1] = near[k + 1], near[k]
        for name, data in (("nearly sorted", near), ("random", rand)):
            print(f"{n:>7} {name:>14} {insertion_comparisons(data):>12,} "
                  f"{timsort_comparisons(data):>10,} {n * n // 4:>12,}")
    print("n = 50,000 random: insertion sort would need about "
          f"{50000 * 50000 // 4:,} comparisons (n^2/4).")


# ---------------- blocklist lookups ----------------------------------------
def blocklist_table():
    rng = random.Random(11)
    size, queries_n = 5000, 50000
    bl = [f"10.{rng.randrange(256)}.{rng.randrange(256)}.{rng.randrange(256)}" for _ in range(size)]
    bl = list(dict.fromkeys(bl))
    pos = {ip: k for k, ip in enumerate(bl)}
    qs = [rng.choice(bl) if rng.random() < 0.5 else
          f"192.168.{rng.randrange(256)}.{rng.randrange(256)}" for _ in range(queries_n)]
    # comparisons by sequential search: position + 1 on a hit, len on a miss
    lin = sum(pos[q] + 1 if q in pos else len(bl) for q in qs)
    t0 = time.perf_counter()
    for q in qs:
        q in bl
    t1 = time.perf_counter()
    s = frozenset(bl)
    for q in qs:
        q in s
    t2 = time.perf_counter()
    print("\n== is_blocked: blocklist of %d IPs, %d lookups (50%% hits) ==" % (len(bl), queries_n))
    print(f"sequential: {lin:,} comparisons, {t1 - t0:.3f} s   |   "
          f"hash set: {queries_n:,} lookups (~1 probe each), {t2 - t1:.4f} s")


# ---------------- signature search: character comparisons ------------------
def sig_compare_count(log, pat):
    n, m = len(log), len(pat)
    if m == 0 or m > n:
        return 0, 0
    cmp = 0
    for i in range(n - m + 1):
        for j in range(m):
            cmp += 1
            if log[i + j] != pat[j]:
                break
    return cmp, n - m + 1


def signature_table():
    print("\n== find_signature: character comparisons ==")
    for label, log, pat in (
        ("sample FAILFAIXFAIL / FAIL", "FAILFAIXFAIL", "FAIL"),
        ("random text n=100,000, m=4", "".join(random.Random(5).choice("abcdefgh") for _ in range(100000)), "abcd"),
        ("worst case a^10000 / a^99 b", "a" * 10000, "a" * 99 + "b"),
    ):
        c, w = sig_compare_count(log, pat)
        print(f"{label:<30} windows={w:>6,}  comparisons={c:>9,}  n*m={len(log) * len(pat):>10,}")


if __name__ == "__main__":
    closest_pair_table()
    sort_table()
    blocklist_table()
    signature_table()
