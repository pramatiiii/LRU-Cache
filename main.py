"""
main.py

Entry point. Runs a short scripted demo of the LRU cache so you can
see put/get/eviction behaviour without typing anything, then
optionally drops into the interactive CLI.

Usage:
    python main.py            # run the demo only
    python main.py --cli      # run the demo, then open interactive CLI
"""

import sys

from cache.lru_cache import LRUCache
from visualizer.render import render_text


def run_demo() -> None:
    print("=== LRU Cache Demo (capacity = 3) ===\n")
    cache = LRUCache(capacity=3)

    steps = [
        ("put", 1, "A"),
        ("put", 2, "B"),
        ("put", 3, "C"),
        ("get", 1, None),      # touching 1 makes it MRU again
        ("put", 4, "D"),       # capacity exceeded -> evicts LRU (which is 2)
        ("get", 2, None),      # should be a MISS, since 2 was evicted
    ]

    for step in steps:
        action, key, value = step
        if action == "put":
            cache.put(key, value)
            print(f"put({key}, {value!r})")
        elif action == "get":
            result = cache.get(key)
            outcome = "MISS" if result is None else f"HIT ({result})"
            print(f"get({key})  ->  {outcome}")
        print(f"    state: {render_text(cache)}\n")

    print("=== Demo complete ===")


if __name__ == "__main__":
    run_demo()

    if "--cli" in sys.argv:
        from cli import run_cli

        interactive_cache = LRUCache(capacity=3)
        print("\nStarting interactive session with a FRESH cache (capacity = 3)...\n")
        run_cli(interactive_cache)
