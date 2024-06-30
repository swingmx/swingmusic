import locale
from typing import TypeVar

T = TypeVar("T")

# Set to user's default locale:
locale.setlocale(locale.LC_ALL, "")

# Or set to a specific locale:
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def format_number(number: float) -> str:
    return locale.format_string("%d", number, grouping=True)




def flatten(list_: list[list[T]]) -> list[T]:
    return [item for sublist in list_ for item in sublist]
