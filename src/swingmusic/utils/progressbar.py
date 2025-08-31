from tqdm import tqdm as _tqdm


def tqdm(*args, **kwargs):
    """
    Wrapper for tqdm that sets globals.
    """
    bar_format = "{percentage:3.0f}%|{bar:45}|{n_fmt}/{total_fmt}{desc}"
    kwargs["bar_format"] = bar_format

    if "desc" in kwargs:
        print(f'INFO|{kwargs["desc"].capitalize()} ...')
        kwargs["desc"] = ""


    return _tqdm(*args, **kwargs)
