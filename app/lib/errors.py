class PopulateCancelledError(Exception):
    """
    Raised when the instance key of a looping function called
    inside Populate is changed.
    """

    pass
