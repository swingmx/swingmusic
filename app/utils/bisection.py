class UseBisection:
    """
    Uses bisection to find a list of items in another list.

    returns a list of found items with `None` items being not found
    items.
    """

    def __init__(self, source: list, search_from: str, queries: list[str]) -> None:
        self.source_list = source
        self.queries_list = queries
        self.attr = search_from

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

    def __call__(self) -> list:
        if len(self.source_list) == 0:
            return [None]

        return [self.find(query) for query in self.queries_list]


def bisection_search_string(strings: list[str], target: str) -> str | None:
    """
    Finds a string in a list of strings using bisection search.
    """
    if not strings:
        return None

    strings = sorted(strings)

    left = 0
    right = len(strings) - 1
    while left <= right:
        middle = (left + right) // 2
        if strings[middle] == target:
            return strings[middle]

        if strings[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return None
