from app.models.track import Track


class UseBisection:
    """
    Uses bisection to find a list of items in another list.

    returns a list of found items with `None` items being not found
    items.
    """

    def __init__(
        self, source: list, search_from: str, queries: list[str], limit=-1
    ) -> None:
        self.source_list = source
        self.queries_list = queries
        self.attr = search_from
        self.limit = limit

    def find(self, query: str):
        left = 0
        right = len(self.source_list) - 1

        while left <= right:
            mid = (left + right) // 2
            if self.source_list[mid].__getattribute__(self.attr) == query:
                return self.source_list[mid]
            elif self.source_list[mid].__getattribute__(self.attr) > query:
                right = mid - 1
            else:
                left = mid + 1

        return None

    def __call__(self):
        if len(self.source_list) == 0:
            return []

        results: list[Track] = []

        for query in self.queries_list:
            res = self.find(query)

            if res is None:
                continue

            results.append(res)

            if self.limit != -1 and len(results) >= self.limit:
                break

        return results
