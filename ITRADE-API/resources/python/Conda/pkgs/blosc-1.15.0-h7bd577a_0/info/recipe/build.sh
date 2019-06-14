#!/bin/bash

mkdir build
cd build

cmake -G "Unix Makefiles" \
      -DCMAKE_BUILD_TYPE="Release" \
      -DCMAKE_INSTALL_PREFIX="${PREFIX}" \
      -DCMAKE_POSITION_INDEPENDENT_CODE=1 \
      -DBUILD_STATIC=1 \
      -DBUILD_SHARED=1 \
      -DBUILD_TESTS=1 \
      -DBUILD_BENCHMARKS=0 \
      -DPREFER_EXTERNAL_SNAPPY:BOOL=ON \
      -DPREFER_EXTERNAL_LZ4:BOOL=ON \
      -DPREFER_EXTERNAL_ZLIB:BOOL=ON \
      CMAKE_CXX=${CXX} \
      CMAKE_CC=${CC} \
      "${SRC_DIR}"

cmake --build .
cmake --build . --target install
ctest
