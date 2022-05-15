def split_iterable(iterable, w):
    splitted = []
    l = 0
    r = w
    while r < len(iterable):
        splitted.append(tuple(iterable[l:r]))
        l += w
        r += w
    splitted.append(tuple(iterable[r-w:]))
    return splitted