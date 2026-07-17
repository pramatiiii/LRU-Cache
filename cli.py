"""
cli.py

Interactive terminal menu for the LRU cache. Lets you type commands
and watch the internal state (via visualizer/render.py) change in
real time — this is the best way to build intuition for what the
put()/get() pointer logic is actually doing.

Run with:
    python main.py --cli
"""

from cache.lru_cache import LRUCache
from visualizer.render import render_text


MENU = """
========================================
  LRU Cache - Interactive CLI
========================================
  1. put <key> <value>
  2. get <key>
  3. peek <key>          (view without affecting order)
  4. show                (display current cache state)
  5. size                (show current item count / capacity)
  6. help                (show this menu again)
  7. exit
========================================
"""


def run_cli(cache: LRUCache) -> None:
    print(MENU)
    while True:
        raw = input("lru> ").strip()
        if not raw:
            continue

        parts = raw.split()
        command = parts[0].lower()

        if command == "exit":
            print("Goodbye.")
            break

        elif command == "help":
            print(MENU)

        elif command == "show":
            print(render_text(cache))

        elif command == "size":
            print(f"{len(cache)} / {cache.capacity} items")

        elif command == "put":
            if len(parts) < 3:
                print("Usage: put <key> <value>")
                continue
            key, value = parts[1], parts[2]
            cache.put(key, value)
            print(f"put({key}, {value})  ->  {render_text(cache)}")

        elif command == "get":
            if len(parts) < 2:
                print("Usage: get <key>")
                continue
            key = parts[1]
            result = cache.get(key)
            if result is None:
                print(f"get({key})  ->  MISS")
            else:
                print(f"get({key})  ->  HIT: {result}")
            print(render_text(cache))

        elif command == "peek":
            if len(parts) < 2:
                print("Usage: peek <key>")
                continue
            key = parts[1]
            result = cache.peek(key)
            print(f"peek({key})  ->  {result if result is not None else 'not found'}")

        else:
            print(f"Unknown command: {command}. Type 'help' for options.")


if __name__ == "__main__":
    demo_cache = LRUCache(capacity=3)
    run_cli(demo_cache)
