"""Part (b): the ORIGINAL module with only the nine defects corrected.

Each fix is marked  # FIX n  so it can be traced back to the defect table.
No restructuring or optimisation is done here (that is Part (c)).
"""
import math


def sort_alerts(alerts):  # insertion sort by severity, highest first
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0 and alerts[j][1] < key[1]:   # FIX 1: j >= 0 (index 0 must be compared)
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j + 1] = key                       # FIX 2: drop key into the gap at j + 1
    return alerts


def is_blocked(blocklist, ip):  # sequential search
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return True                           # FIX 3: a match means BLOCKED
    return False                                  # searched everything: not on the list


def find_signature(log, pattern):  # brute-force string matching, all occurrences
    n, m = len(log), len(pattern)
    hits = []
    if m == 0 or m > n:                           # boundary guard (empty / too-long pattern)
        return hits
    for i in range(n - m + 1):                    # FIX 4: last start index is n - m (inclusive)
        for j in range(m):
            if log[i + j] != pattern[j]:
                break
        else:                                     # FIX 5: for-else -> only runs if NO mismatch
            hits.append(i)
    return hits


def closest_logins(events):  # brute-force closest pair of login locations
    if len(events) < 2:                           # boundary guard (fewer than two events)
        return None, None
    min_dist = math.inf                           # FIX 6: start at +infinity, not 0
    pair = None
    for i in range(len(events)):
        for j in range(i + 1, len(events)):       # FIX 8 + FIX 9: j > i removes self (i,i) and mirrored (j,i) pairs
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            if d < min_dist:                      # FIX 7: closest means SMALLEST, so '<'
                min_dist = d
                pair = (i, j)
    return pair, min_dist


if __name__ == "__main__":
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    log, pattern = "FAILFAIXFAIL", "FAIL"
    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

    print("sort_alerts    :", sort_alerts(list(alerts)))
    print("is_blocked     :", [(q, is_blocked(blocklist, q)) for q in queries])
    print("find_signature :", find_signature(log, pattern))
    print("closest_logins :", closest_logins(events))
    print("-- boundary tests --")
    print("sort equal sev :", sort_alerts([("E1", 5), ("E2", 5), ("E3", 5)]))
    print("sort empty/one :", sort_alerts([]), sort_alerts([("X", 1)]))
    print("blocked empty  :", is_blocked([], "1.1.1.1"))
    print("sig at end     :", find_signature("xxFAIL", "FAIL"))
    print("sig longer     :", find_signature("ab", "abcd"))
    print("sig == log     :", find_signature("FAIL", "FAIL"))
    print("sig empty pat  :", find_signature("abc", ""))
    print("closest 1 / 0  :", closest_logins([(1, 1)]), closest_logins([]))
    print("closest dup pts:", closest_logins([(1, 1), (9, 9), (1, 1)]))
