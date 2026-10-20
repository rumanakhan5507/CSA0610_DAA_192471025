"""Test harness for sentinelops.py  -  run:  python -m unittest -v test_sentinelops"""
import random
import unittest

from sentinelops import (
    sort_alerts, sort_alerts_insertion, build_blocklist, is_blocked,
    find_signature, closest_logins, closest_logins_bruteforce,
)

ALERTS = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
BLOCKLIST = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
EVENTS = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]


class TestSortAlerts(unittest.TestCase):
    EXPECTED = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]

    def test_sample(self):
        self.assertEqual(sort_alerts(list(ALERTS)), self.EXPECTED)
        self.assertEqual(sort_alerts_insertion(list(ALERTS)), self.EXPECTED)

    def test_no_alert_lost_or_duplicated(self):
        self.assertCountEqual(sort_alerts(list(ALERTS)), ALERTS)

    def test_equal_severity_keeps_arrival_order(self):
        data = [("E1", 5), ("E2", 5), ("E3", 5)]
        self.assertEqual(sort_alerts(list(data)), data)
        self.assertEqual(sort_alerts_insertion(list(data)), data)

    def test_empty_and_single(self):
        self.assertEqual(sort_alerts([]), [])
        self.assertEqual(sort_alerts([("X", 1)]), [("X", 1)])

    def test_already_sorted_and_reversed(self):
        desc = [("a", 9), ("b", 7), ("c", 2)]
        self.assertEqual(sort_alerts(list(desc)), desc)
        self.assertEqual(sort_alerts(list(reversed(desc))), desc)

    def test_random_matches_baseline(self):
        rng = random.Random(1)
        for _ in range(200):
            data = [(f"a{k}", rng.randint(1, 6)) for k in range(rng.randint(0, 40))]
            self.assertEqual(sort_alerts(list(data)), sort_alerts_insertion(list(data)))


class TestIsBlocked(unittest.TestCase):
    def test_sample_list_and_set(self):
        for bl in (BLOCKLIST, build_blocklist(BLOCKLIST)):
            self.assertTrue(is_blocked(bl, "10.0.0.9"))
            self.assertTrue(is_blocked(bl, "10.0.0.5"))
            self.assertFalse(is_blocked(bl, "8.8.8.8"))

    def test_first_middle_last(self):
        for ip in BLOCKLIST:
            self.assertTrue(is_blocked(BLOCKLIST, ip))

    def test_empty_blocklist(self):
        self.assertFalse(is_blocked([], "1.1.1.1"))
        self.assertFalse(is_blocked(build_blocklist([]), "1.1.1.1"))


class TestFindSignature(unittest.TestCase):
    def test_sample(self):
        self.assertEqual(find_signature("FAILFAIXFAIL", "FAIL"), [0, 8])

    def test_pattern_at_very_end(self):
        self.assertEqual(find_signature("xxFAIL", "FAIL"), [2])

    def test_pattern_at_very_start(self):
        self.assertEqual(find_signature("FAILxx", "FAIL"), [0])

    def test_no_false_hit_when_last_char_differs(self):
        self.assertEqual(find_signature("FAIX", "FAIL"), [])

    def test_pattern_longer_than_log(self):
        self.assertEqual(find_signature("ab", "abcd"), [])

    def test_pattern_equals_log(self):
        self.assertEqual(find_signature("FAIL", "FAIL"), [0])

    def test_overlapping_matches(self):
        self.assertEqual(find_signature("aaaa", "aa"), [0, 1, 2])

    def test_empty_log_and_empty_pattern(self):
        self.assertEqual(find_signature("", "FAIL"), [])
        self.assertEqual(find_signature("abc", ""), [])

    def test_matches_str_find_on_random_text(self):
        rng = random.Random(2)
        for _ in range(300):
            log = "".join(rng.choice("ab") for _ in range(rng.randint(0, 30)))
            pat = "".join(rng.choice("ab") for _ in range(rng.randint(1, 4)))
            expected = [i for i in range(len(log) - len(pat) + 1) if log.startswith(pat, i)]
            self.assertEqual(find_signature(log, pat), expected)


class TestClosestLogins(unittest.TestCase):
    def test_sample(self):
        pair, dist = closest_logins(EVENTS)
        self.assertEqual(pair, (0, 5))
        self.assertAlmostEqual(dist, 2 ** 0.5)
        self.assertEqual(closest_logins_bruteforce(EVENTS), (pair, dist))

    def test_fewer_than_two_events(self):
        self.assertEqual(closest_logins([]), (None, None))
        self.assertEqual(closest_logins([(1, 1)]), (None, None))

    def test_exactly_two_events(self):
        self.assertEqual(closest_logins([(0, 0), (3, 4)]), ((0, 1), 5.0))

    def test_duplicate_locations_give_zero(self):
        self.assertEqual(closest_logins([(1, 1), (9, 9), (1, 1)]), ((0, 2), 0.0))

    def test_same_x_vertical_line(self):
        self.assertEqual(closest_logins([(5, 0), (5, 10), (5, 11)]), ((1, 2), 1.0))

    def test_ties_match_bruteforce(self):
        ev = [(0, 0), (1, 0), (5, 5), (6, 5), (0, 1)]       # several pairs at distance 1
        self.assertEqual(closest_logins(ev), closest_logins_bruteforce(ev))

    def test_random_matches_bruteforce(self):
        rng = random.Random(3)
        for _ in range(300):
            ev = [(rng.randint(0, 25), rng.randint(0, 25)) for _ in range(rng.randint(2, 40))]
            self.assertEqual(closest_logins(ev), closest_logins_bruteforce(ev))


if __name__ == "__main__":
    unittest.main(verbosity=2)
