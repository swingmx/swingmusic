import string
import random


def get_random_str(length=5):
    """
    Generates a random string of length `length`.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
