import pytest
from .. import split_iterable


@pytest.mark.parametrize(
    'iterable, width, expected_splitted',(
    (
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 5, [(1, 2, 3, 4, 5), (6, 7, 8, 9, 10)],
    ),
    (
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 20, [(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)],
    ),
    (
        [], 2, [()],
    ),
    (
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), 7, [(1, 2, 3, 4, 5, 6, 7), (8, 9, 10)],
    ),
))
def test_squarify_string(iterable, width, expected_splitted):
    splitted = split_iterable(iterable, width)
    assert splitted == expected_splitted