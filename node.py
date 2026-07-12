"""
lru_cache.py

The core engine of this project. Combines:
    1. A hash map (Python dict)   -> O(1) lookup: key -> Node
    2. A doubly linked list       -> O(1) reordering (most-recently-used
                                      at the front, least-recently-used
                                      at the back)

Why sentinel (dummy) head/tail nodes?
--------------------------------------
Without sentinels, inserting into or removing from an EMPTY list, or a
list with only ONE node, requires special-case handling (checking for
None in several places). By keeping two permanent dummy nodes -
self.head and self.tail - that never hold real data, every real node
always has a valid prev and a valid next. This removes a whole class
of edge-case bugs. This is a common, deliberate trick in linked-list
implementations, not just decoration.

Layout of the list at all times:

    head <-> [MRU node] <-> ... <-> [LRU node] <-> tail

    - Nodes are added right after `head` (most recently used position)
    - Nodes are evicted from right before `tail` (least recently used)
"""

from typing import Any, Dict, Optional

from cache.node import Node


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")

        self.capacity = capacity
        self.map: Dict[Any, Node] = {}

        # Sentinel nodes. They never hold real key/value data.
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: Any) -> Optional[Any]:
        """
        Return the value for `key` if present, else None.
        Accessing a key counts as "using" it, so we move it to the
        front (most-recently-used position).
        """
        if key not in self.map:
            return None

        node = self.map[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update the value for `key`.
        If the key already exists, update its value and move it to
        the front. If the cache is at capacity and this is a NEW key,
        evict the least-recently-used node first.
        """
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            return

        if len(self.map) >= self.capacity:
            self._evict_lru()

        new_node = Node(key, value)
        self.map[key] = new_node
        self._add_to_front(new_node)

    def peek(self, key: Any) -> Optional[Any]:
        """
        Like get(), but does NOT affect recency ordering.
        Useful for inspection/debugging without disturbing the cache.
        """
        node = self.map.get(key)
        return node.value if node else None

    def __contains__(self, key: Any) -> bool:
        return key in self.map

    def __len__(self) -> int:
        return len(self.map)

    def keys_in_order(self) -> list:
        """
        Returns keys ordered from most-recently-used to
        least-recently-used. Primarily for the CLI/visualizer and tests.
        """
        result = []
        current = self.head.next
        while current is not self.tail:
            result.append(current.key)
            current = current.next
        return result

    # ------------------------------------------------------------------
    # Internal helpers (all O(1))
    # ------------------------------------------------------------------

    def _remove(self, node: Node) -> None:
        """Unlink `node` from the list. Does NOT touch the hash map."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        node.prev = None
        node.next = None

    def _add_to_front(self, node: Node) -> None:
        """Insert `node` immediately after head (MRU position)."""
        old_first = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = old_first
        old_first.prev = node

    def _evict_lru(self) -> None:
        """Remove the node immediately before tail (LRU position)."""
        lru_node = self.tail.prev
        if lru_node is self.head:
            return  # cache is empty, nothing to evict
        self._remove(lru_node)
        del self.map[lru_node.key]
