def coroutine(func):
    """
    Decorator: primes `func` by advancing to first `yield`
    """

    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start
