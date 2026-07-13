"""
render.py

Renders the current state of an LRUCache so you can SEE the pointer
logic working, rather than just trusting it. Watching eviction happen
visually is what makes the O(1) linked-list logic click.

Two render modes:
    render_text(cache)  -> always available, no dependencies
    render_image(cache)  -> optional, requires matplotlib
"""

from cache.lru_cache import LRUCache


def render_text(cache: LRUCache) -> str:
    """
    Returns a single-line text diagram, ordered from most-recently-used
    (left) to least-recently-used (right). Example:

        [MRU] 3:apple <-> 1:banana <-> 5:cherry [LRU]
    """
    keys_in_order = cache.keys_in_order()

    if not keys_in_order:
        return "[empty cache]"

    parts = [f"{k}:{cache.peek(k)}" for k in keys_in_order]
    body = " <-> ".join(parts)
    return f"[MRU] {body} [LRU]"


def render_image(cache: LRUCache, path: str = "cache_state.png") -> str:
    """
    Renders the cache as a simple horizontal box diagram using
    matplotlib and saves it to `path`. Requires matplotlib to be
    installed. Returns the path the image was saved to.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required for render_image(). "
            "Install it with: pip install matplotlib"
        ) from exc

    keys_in_order = cache.keys_in_order()

    fig, ax = plt.subplots(figsize=(max(4, len(keys_in_order) * 2), 2))
    ax.axis("off")

    if not keys_in_order:
        ax.text(0.5, 0.5, "empty cache", ha="center", va="center", fontsize=14)
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        return path

    box_width = 1.5
    spacing = 0.5
    x = 0

    for key in keys_in_order:
        value = cache.peek(key)
        ax.add_patch(
            plt.Rectangle((x, 0), box_width, 1, fill=True, facecolor="#dbe9ff", edgecolor="black")
        )
        ax.text(x + box_width / 2, 0.5, f"{key}\n{value}", ha="center", va="center", fontsize=10)
        x += box_width + spacing

    ax.text(0 - 0.1, 1.15, "MRU", fontsize=9, ha="left", color="green")
    ax.text(x - spacing - 0.1, 1.15, "LRU", fontsize=9, ha="right", color="red")

    ax.set_xlim(-0.5, x)
    ax.set_ylim(-0.5, 1.8)

    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path
