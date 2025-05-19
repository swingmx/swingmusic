from typing import Iterator


class CustomList(list):
    # TODO: I think SharedMemoryList implementation will be done here.
    # This list should be used as a normal list without any changes in the stores.

    def __getitem__(self, index):
        # Do some shared memory stuff here
        # print the length of the list
        # print(f"__getitem__ Length of the list: {len(self)}")
        return super().__getitem__(index)

    def __iter__(self) -> Iterator:
        # Do some shared memory stuff here
        # print the length of the list
        # print(f"__iter__ Length of the list: {len(self)}")
        return super().__iter__()
