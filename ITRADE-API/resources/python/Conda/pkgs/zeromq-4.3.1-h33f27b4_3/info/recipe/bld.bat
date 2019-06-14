echo #include ^<stdint.h^> > src\stdint.hpp
mkdir build
cd build

cmake -G "NMake Makefiles"                        ^
      -D CMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX%    ^
      -D WITH_LIBSODIUM=ON                        ^
      -D ENABLE_DRAFTS=OFF                        ^
      -D WITH_PERF_TOOL=OFF                       ^
      -D ZMQ_BUILD_TESTS=ON                       ^
      -D ENABLE_CPACK=OFF                         ^
      -D CMAKE_BUILD_TYPE=Release                 ^
      -D CMAKE_EXE_LINKER_FLAGS='-STACK:8388608'  ^
      ..
if %errorlevel% neq 0 exit /b %errorlevel%

nmake install
if %errorlevel% neq 0 exit /b %errorlevel%

:: Copy of dll and import library on windows (required by pyzmq)
copy /y %LIBRARY_BIN%\libzmq-mt-4*.dll /b %LIBRARY_BIN%\libzmq.dll
if %errorlevel% neq 0 exit /b %errorlevel%
copy /y %LIBRARY_LIB%\libzmq-mt-4*.lib /b %LIBRARY_LIB%\libzmq.lib
if %errorlevel% neq 0 exit /b %errorlevel%

ctest -C Release -V
if %errorlevel% neq 0 exit /b %errorlevel%
