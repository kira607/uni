class _Missing(object):
    def __str__(self):
        return f'{self.__class__.__name__}'

    def __repr__(self):
        return f'<{str(self)}>'

    def __copy__(self):
        return self

    def __deepcopy__(self):
        return self


MISSING = _Missing()
