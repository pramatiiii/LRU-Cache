LRU Cache From Scratch
A hand-built Least Recently Used (LRU) cache implemented in pure Python, combining a hash map and a doubly linked list to achieve O(1) get/put operations. Includes an interactive CLI to watch the cache's internal ordering change live, a text/image visualizer, a full pytest suite, and a benchmark comparing it against Python's built-in OrderedDict-based approach.

What the project does
Implements an LRUCache class from first principles — no OrderedDict, no functools.lru_cache, no shortcuts
Combines a Python dict (O(1) key lookup) with a custom doubly linked list (O(1) reordering) so both get() and put() run in O(1)
Evicts the least-recently-used entry automatically once the cache reaches capacity
Provides an interactive terminal CLI to put/get/inspect the cache and watch its ordering change in real time
Renders the current cache state as a text diagram, or optionally a PNG image
Benchmarks the hand-built version against collections.OrderedDict to confirm the O(1) claims hold up in practice
Project structure
lru_cache/
│
├── main.py                     ← Entry point. Runs a scripted demo, then optionally the CLI.
├── cli.py                      ← Interactive CLI menu to put/get/inspect the cache live
│
├── cache/
│   ├── __init__.py
│   ├── node.py                 ← Node class (one entry in the doubly linked list)
│   └── lru_cache.py            ← LRUCache class — the hash map + linked list logic
│
├── visualizer/
│   ├── __init__.py
│   └── render.py                ← Renders the cache's current state as text or a PNG image
│
├── tests/
│   ├── __init__.py
│   └── test_lru_cache.py       ← Unit tests: correctness, eviction order, edge cases
│
├── benchmark.py                 ← Compares hand-built cache speed vs OrderedDict/functools.lru_cache
└── requirements.txt              ← Python dependencies
Setup and installation
Step 1 — Install Python
This project requires Python 3.8 or higher. Check your version: python --version

Step 2 — Install dependencies
pip install -r requirements.txt
Or install manually:

pip install pytest matplotlib
Note: the core cache (cache/node.py, cache/lru_cache.py) has zero external dependencies. pytest is only needed to run the tests, and matplotlib is only needed for the optional image visualizer.

Step 3 — Run the application
# Run the scripted demo and exit:
python main.py

# Run the demo, then open the interactive CLI:
python main.py --cli

# Run the test suite:
pytest -v

# Run the benchmark against OrderedDict:
python benchmark.py
CLI menu options
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
Core API
Method	Behaviour	Time complexity
get(key)	Returns the value if present, else None. Marks the key as most-recently-used.	O(1)
put(key, value)	Inserts or updates a key. Evicts the least-recently-used entry if the cache is full.	O(1)
peek(key)	Returns the value without affecting recency order. Useful for debugging/inspection.	O(1)
keys_in_order()	Returns all keys ordered from most-recently-used to least-recently-used.	O(n)
Libraries used
Built-in (no installation needed)
Library	Used for
typing	Type hints on Node and LRUCache for self-documenting interfaces
collections.OrderedDict	Only in benchmark.py, as the comparison baseline — not used in the core cache
functools	Only in benchmark.py, for comparing against the lru_cache decorator
time	Measuring benchmark performance
External (install via pip)
Library	Used for
pytest	Writing and running the unit test suite
matplotlib	Optional — rendering the cache state as a PNG image instead of text
Key concepts used in this project
Concept	Where it appears
Hash map + doubly linked list	Core design of cache/lru_cache.py — each structure covers the other's weakness
Sentinel (dummy) nodes	self.head / self.tail in LRUCache.__init__ — removes edge-case handling for empty/single-node lists
Pointer manipulation	_remove() and _add_to_front() in lru_cache.py
Encapsulation	Internal helpers prefixed with _ signal "implementation detail, not public API"
Dunder methods	__len__ and __contains__ on LRUCache, __repr__ on Node
O(1) vs O(n) reasoning	Why a dict alone or a linked list alone cannot solve this problem on its own
Unit testing with pytest	tests/test_lru_cache.py — correctness, eviction order, and edge cases like capacity=1
Benchmarking	benchmark.py — timing comparison against collections.OrderedDict
Event loop	while True + break pattern in cli.py
matplotlib patches	Rectangle-based diagram rendering in visualizer/render.py (optional path)
How to extend this project
Add TTL (time-based expiry) → store an insertion/access timestamp on each Node and check it in get()
Add thread-safety → wrap put()/get() with a threading.Lock for concurrent access
Add persistence → serialize the cache to disk (e.g. with pickle or json) on shutdown and reload on startup
Add an LFU (Least Frequently Used) variant → track access counts instead of recency, for comparison
Wrap it as a decorator → similar to functools.lru_cache, so it can cache function call results directly
Add a new CLI command → add an elif branch in cli.py
Requirements
See requirements.txt:

pytest>=7.0.0
matplotlib>=3.6.0
