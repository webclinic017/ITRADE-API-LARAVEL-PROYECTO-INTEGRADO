for /F "usebackq" %%i in (`dir /s /b *.pyx`) do touch %%i
%PYTHON% setup.py cython
%PYTHON% -m pip install --no-deps --ignore-installed -v .
