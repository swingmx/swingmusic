import threading


def background(func):
    """
    Runs the decorated function in a background thread.
    """

    def background_func(*a, **kw):
        threading.Thread(target=func, args=a, kwargs=kw).start()

    return background_func


class ThreadWithReturnValue(threading.Thread):
    """
    A thread class that returns a value on join.

    Credit: https://stackoverflow.com/a/6894023
    """

    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None
    ):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return
