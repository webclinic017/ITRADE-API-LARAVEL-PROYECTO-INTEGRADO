#!/bin/bash


# Use OpenBLAS with 1 thread only as it seems to be using too many
# on the CIs apparently.
export OPENBLAS_NUM_THREADS=1

# # Depending on our platform, shared libraries end with either .so or .dylib
if [[ $(uname) == 'Darwin' ]]; then
    export LDFLAGS="$LDFLAGS -undefined dynamic_lookup"
else
    export LDFLAGS="$LDFLAGS -shared"
fi

cp $PREFIX/site.cfg site.cfg

$PYTHON setup.py install --single-version-externally-managed --record=record.txt
