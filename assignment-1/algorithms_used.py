"""Search algorithms for DAA Assignment 1.

Each search returns (found, comparisons), except binary_search_recursive,
which also uses a mutable counter so the number of comparisons is available
after recursive calls.
"""


def linear_search(arr, key):
    """Iterative linear search. Returns (found, comparisons)."""
    comparisons = 0
    for value in arr:
        comparisons += 1
        if value == key:
            return True, comparisons
    return False, comparisons


def binary_search_recursive(arr, key, low=0, high=None, counter=None):
    """Recursive binary search on a sorted array.

    Returns True/False. `counter` should be a one-item list, e.g. [0],
    to count key comparisons across recursive calls.
    """
    if high is None:
        high = len(arr) - 1
    if counter is None:
        counter = [0]

    if low > high:
        return False

    mid = (low + high) // 2
    counter[0] += 1

    if arr[mid] == key:
        return True
    if key < arr[mid]:
        return binary_search_recursive(arr, key, low, mid - 1, counter)
    return binary_search_recursive(arr, key, mid + 1, high, counter)


class HashTableChaining:
    """Hash table using key % table_size and separate chaining."""

    def __init__(self, n):
        # Keep the table size odd and target a load factor close to 0.75.
        self.size = max(8, int(n / 0.75)) | 1
        self.table = [None] * self.size

    def add(self, key):
        index = key % self.size
        if self.table[index] is None:
            self.table[index] = [key]
        else:
            self.table[index].append(key)

    def find(self, key):
        """Returns (found, comparisons). Empty bucket means zero comparisons."""
        comparisons = 0
        bucket = self.table[key % self.size]
        if bucket is None:
            return False, comparisons

        for value in bucket:
            comparisons += 1
            if value == key:
                return True, comparisons
        return False, comparisons
