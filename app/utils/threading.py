import threading


def background(func):
    """
    Runs the decorated function in a background thread.
    """

    def background_func(*a, **kw):
        threading.Thread(target=func, args=a, kwargs=kw).start()

    return background_func
