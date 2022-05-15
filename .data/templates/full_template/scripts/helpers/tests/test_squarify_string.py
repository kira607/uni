import pytest
from .. import squarify_string


@pytest.mark.parametrize(
    'string, width, expected_squared_string',(
    (
        'aaabbbcccdddeeefff', 3, 'aaa\nbbb\nccc\nddd\neee\nfff',
    ),
    (
        'aaaabbbbcc', 4, 'aaaa\nbbbb\ncc',
    ),
    (
        'aaaabbbbccccc', 4, 'aaaa\nbbbb\ncccc\nc',
    ),
    (
        'aaabbbccc', 20, 'aaabbbccc',
    ),
    (
    '1111111101000100001010111111110001101100110101010010010111000110011000100101110110111'
    '1010000011111001110111100001010110010011010001110101011001110000110010111001001000011'
    '1101011100011010000010000101111001001010101111100110101100000001101000110111001110110',
    85,
    '1111111101000100001010111111110001101100110101010010010111000110011000100101110110111\n'
    '1010000011111001110111100001010110010011010001110101011001110000110010111001001000011\n'
    '1101011100011010000010000101111001001010101111100110101100000001101000110111001110110',
    ),
))
def test_squarify_string(string, width, expected_squared_string):
    squared = squarify_string(string, width)
    s2 = ''.join(squared.split('\n'))

    assert squared == expected_squared_string
    assert len(s2) == len(string)
    assert s2 == string