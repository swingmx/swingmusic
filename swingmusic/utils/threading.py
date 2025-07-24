import threading
from multiprocessing import Process, Pipe


def background(func):
    """
    Runs the decorated function in a background thread.
    """

    def background_func(*a, **kw):
        threading.Thread(target=func, args=a, kwargs=kw).start()

    return background_func



class ProcessWithReturnValue(Process):
    """
    A process class that returns a value on join.
    Uses a pipe to communicate the return value back to the parent process.
    """

    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None
    ):
        Process.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
        self._parent_conn, self._child_conn = Pipe()
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def run(self):
        if self._target is not None:
            result = self._target(*self._args, **self._kwargs)
            self._child_conn.send(result)
        self._child_conn.close()

    def join(self, *args):
        Process.join(self, *args)
        if self._parent_conn.poll():
            return self._parent_conn.recv()
        return None