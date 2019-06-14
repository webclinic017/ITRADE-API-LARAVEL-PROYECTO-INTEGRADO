import unittest

from hypothesis import given, note
from hypothesis.strategies import binary, lists, integers, tuples, just

from backports.os import _chunks


class TestChunks(unittest.TestCase):
    """
    Test the `_chunks()` helper.
    """

    # Strategy for pairs of bytes and lists of ascending indexes into them.
    _bytes_and_indexes = binary(min_size=1).flatmap(
        lambda b: tuples(just(b),
                         lists(integers(0, len(b) - 1), unique=True).map(sorted)))

    @given(_bytes_and_indexes)
    def test_identity(self, b_indexes):
        """
        b''.join(_chunks(b, indexes)) == b
        """
        (b, indexes) = b_indexes
        cs = list(_chunks(b, indexes))
        note('chunks = {!r}'.format(cs))
        self.assertEqual(b''.join(_chunks(b, indexes)), b)

    @given(_bytes_and_indexes)
    def test_splits(self, b_indexes):
        """
        The input should be split before and after each indexed character,
        and nowhere else.
        """
        (b, indexes) = b_indexes

        expected_splits = {0, len(b)} | {j for i in indexes
                                           for j in [i, i + 1]}
        cs = list(_chunks(b, indexes))
        note('chunks = {!r}'.format(cs))

        def _splits():
            i = 0
            yield i
            for chunk in cs:
                i += len(chunk)
                yield i
        actual_splits = set(_splits())

        self.assertEqual(expected_splits, actual_splits)
