from typing import List, Optional, TypeVar

T = TypeVar("T")

def use_bisection(
    source: List[T], key: str, queries: List[str], limit: int = -1
) -> List[Optional[T]]:
    """
    Uses bisection to find a list of items in another list.

    Returns a list of found items with `None` items being not found items.
    """

    def find(query: str):
        left = 0
        right = len(source) - 1

        while left <= right:
            mid = (left + right) // 2
            if source[mid].__getattribute__(key) == query:
                return source[mid]
            elif source[mid].__getattribute__(key) > query:
                right = mid - 1
            else:
                left = mid + 1

        return None

    if len(source) == 0:
        return []

    results = []

    for query in queries:
        res = find(query)

        if res is None:
            continue

        results.append(res)

        if limit != -1 and len(results) >= limit:
            break

    return results
