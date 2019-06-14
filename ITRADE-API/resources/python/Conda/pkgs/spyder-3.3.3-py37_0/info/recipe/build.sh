#!/bin/bash

$PYTHON -m pip install . --no-deps --ignore-installed -vvv

rm -rf $PREFIX/man
rm -f $PREFIX/bin/spyder_win_post_install.py
rm -rf $SP_DIR/Sphinx-*

if [[ ($PY3K == 1) && (`uname` == Linux) ]]; then
    BIN=$PREFIX/bin
    mv $BIN/spyder3 $BIN/spyder
fi
