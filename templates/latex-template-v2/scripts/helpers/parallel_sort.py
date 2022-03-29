def parallel_sort(x, y, sort_by='x'):
    d = {}
    for x0, y0 in zip(x, y):
        d[x0] = y0
    d = dict(sorted(d.items()))
    return list(d.keys()), list(d.values())