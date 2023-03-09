import string
from datetime import datetime
import random


def create_new_date():
    """
    It creates a new date and time string in the format of "YYYY-MM-DD HH:MM:SS"
    :return: A string of the current date and time.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_random_str(length=5):
    """
    Generates a random string of length `length`.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
