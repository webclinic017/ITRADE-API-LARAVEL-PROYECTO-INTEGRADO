#!/bin/bash

find pandas -name "*.pyx" -exec touch {} \;
${PYTHON} setup.py cython

# -fno-strict-aliasing is likely essential on clang, and silences lots of warnings on linux
# -fwrapv because that's what Pandas do on their CI:
# https://github.com/pandas-dev/pandas/pull/12946
CFLAGS="${CFLAGS} -fno-strict-aliasing -fwrapv" \
    ${PYTHON} -m pip install --no-deps --ignore-installed -v .
