from .split_iterable import split_iterable


def squarify_string(string, w=30, sep='\n'):
    parts = split_iterable(string, w)
    result = sep.join((''.join(part) for part in parts))
    return result