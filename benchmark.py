"""
benchmark.py

Compares the hand-built LRUCache against Python's built-in
OrderedDict-based approach, to sanity-check that our O(1) claims
actually hold up in practice as the number of operations grows.

This is also where the earlier caveat gets closed: in real production
code, you would normally just use collections.OrderedDict (which
already combines a hash map + doubly linked list internally) rather
than hand-rolling this. We only built our own version above so the
pointer logic itself would be visible and understandable.

Run with:
    python benchmark.py
"""

import time
from collections import OrderedDict

from cache.lru_cache import LRUCache


class OrderedDictLRUCache:
    """
    A minimal LRU cache built on top of OrderedDict, for comparison.
    OrderedDict.move_to_end() and popitem(last=False) give us the same
    O(1) reordering / eviction behaviour "for free."
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: OrderedDict = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return None
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)  # evict LRU (front of OrderedDict)


def time_operations(cache, num_operations: int) -> float:
    start = time.perf_counter()
    for i in range(num_operations):
        cache.put(i % 1000, i)
        cache.get(i % 1000)
    end = time.perf_counter()
    return end - start


def run_benchmark(num_operations: int = 200_000, capacity: int = 1000) -> None:
    print(f"Benchmarking {num_operations:,} put+get operations, capacity={capacity}\n")

    hand_built = LRUCache(capacity=capacity)
    hand_built_time = time_operations(hand_built, num_operations)
    print(f"Hand-built LRUCache      : {hand_built_time:.4f} seconds")

    ordered_dict_based = OrderedDictLRUCache(capacity=capacity)
    ordered_dict_time = time_operations(ordered_dict_based, num_operations)
    print(f"OrderedDict-based cache  : {ordered_dict_time:.4f} seconds")

    print(
        "\nBoth should scale similarly (roughly linear in num_operations), "
        "since both are truly O(1) per operation. If the hand-built "
        "version is dramatically slower or its time grows non-linearly "
        "as num_operations increases, that's a signal something in the "
        "implementation isn't actually O(1) - worth investigating."
    )


if __name__ == "__main__":
    run_benchmark()
