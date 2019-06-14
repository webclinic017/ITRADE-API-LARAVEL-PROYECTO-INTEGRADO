"""
Partial backport of Python 3.5's Lib/test/test_os.py.
"""
from __future__ import unicode_literals

from backports import os

import unittest


class FSEncodingTests(unittest.TestCase):
    def test_nop(self):
        self.assertEqual(os.fsencode(b'abc\xff'), b'abc\xff')
        self.assertEqual(os.fsdecode('abc\u0141'), 'abc\u0141')

    def test_identity(self):
        # assert fsdecode(fsencode(x)) == x
        for fn in ('unicode\u0141', 'latin\xe9', 'ascii'):
            try:
                bytesfn = os.fsencode(fn)
            except UnicodeEncodeError:
                continue

            # XXX backport: Ignore bug in future.utils.surrogateescape.replace_surrogate_encode()
            # by treating the below NameError like the above UnicodeEncodeError.
            #
            # Bug: https://github.com/PythonCharmers/python-future/issues/256
            # (This workaround can be removed once that is fixed.)
            except NameError as e:  # pragma: no cover
                if e.message == "global name 'exc' is not defined":
                    continue
                else:
                    raise

            self.assertEqual(os.fsdecode(bytesfn), fn)
