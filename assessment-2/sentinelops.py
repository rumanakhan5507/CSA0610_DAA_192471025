"""SentinelOps SOC alert-triage module (corrected and optimised).

Functions
---------
sort_alerts          sort alerts by severity, highest first, ties in arrival order
build_blocklist      one-off conversion of a blocklist into a hash set
is_blocked           check whether a source IP is on the blocklist
find_signature       every start position of an attack signature in a log line
closest_logins       closest pair of login locations (pruned brute force)

Reference baselines kept for validation and for the measurements in
analysis.py:  sort_alerts_insertion  and  closest_logins_bruteforce.
"""
import math


# --------------------------------------------------------------------------
# 1. Sorting alerts by severity
# --------------------------------------------------------------------------
def sort_alerts_insertion(alerts):
    """Corrected insertion sort (baseline): severity descending, stable.

    Strict '<' keeps equal severities in arrival order. O(n^2) worst case.
    """
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0 and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j + 1] = key
    return alerts


def sort_alerts(alerts):
    """Sort alerts in place by severity (item[1]), highest first.

    Alerts of equal severity keep their arrival order. Uses Python's Timsort,
    which is stable, O(n log n) worst case and ~O(n) on nearly sorted input.
    `reverse=True` preserves the original order of equal keys.
    """
    alerts.sort(key=lambda alert: alert[1], reverse=True)
    return alerts


# --------------------------------------------------------------------------
# 2. Blocklist lookups
# --------------------------------------------------------------------------
def build_blocklist(blocklist):
    """Return a frozenset of blocked IPs for O(1) average-time lookups.

    Build it ONCE, then reuse it for every query.
    """
    return frozenset(blocklist)


def is_blocked(blocklist, ip):
    """Return True if `ip` is on the blocklist, otherwise False.

    Works with a list (linear scan, stops at the first match) or with the set
    returned by build_blocklist (hash lookup). An empty blocklist gives False.
    """
    return ip in blocklist


# --------------------------------------------------------------------------
# 3. Signature search
# --------------------------------------------------------------------------
def find_signature(log, pattern):
    """Return every start index at which `pattern` occurs in `log`.

    Brute-force matching. Only the n - m + 1 windows that can hold the pattern
    are tried, each window stops at its first mismatch, and no comparison is
    repeated after a mismatch (for/else replaces the old post-loop test).
    An empty pattern or one longer than the log returns [].
    """
    n, m = len(log), len(pattern)
    if m == 0 or m > n:
        return []
    hits = []
    for i in range(n - m + 1):
        for j in range(m):
            if log[i + j] != pattern[j]:
                break
        else:                      # no mismatch in the whole window
            hits.append(i)
    return hits


# --------------------------------------------------------------------------
# 4. Closest pair of login locations
# --------------------------------------------------------------------------
def closest_logins_bruteforce(events):
    """Corrected brute-force closest pair (baseline): every pair once, O(n^2)."""
    if len(events) < 2:
        return None, None
    best, pair = math.inf, None
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            if d < best:
                best, pair = d, (i, j)
    return pair, best


def closest_logins(events):
    """Return ((i, j), distance) for the two closest login locations, i < j.

    Same result as closest_logins_bruteforce, with three savings:
      * each unordered pair is examined once (no self or mirrored pairs);
      * squared distances are compared; sqrt is taken once, at the end;
      * events are visited in x order and the inner loop stops as soon as the
        x-gap alone already exceeds the best distance found so far.
    Ties are resolved to the lexicographically smallest (i, j), matching the
    brute force. Fewer than two events returns (None, None).
    """
    n = len(events)
    if n < 2:
        return None, None
    order = sorted(range(n), key=lambda k: events[k][0])   # indices by x
    best_sq, best_pair = math.inf, None
    for a in range(n - 1):
        i = order[a]
        xi, yi = events[i]
        for b in range(a + 1, n):
            j = order[b]
            dx = events[j][0] - xi
            dx2 = dx * dx
            if dx2 > best_sq:      # x-gap alone is too big: no later j can win
                break
            dy = events[j][1] - yi
            d2 = dx2 + dy * dy
            pair = (i, j) if i < j else (j, i)
            if d2 < best_sq or (d2 == best_sq and pair < best_pair):
                best_sq, best_pair = d2, pair
    return best_pair, math.sqrt(best_sq)
