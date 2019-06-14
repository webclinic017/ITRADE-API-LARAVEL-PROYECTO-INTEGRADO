#  tests for llvmlite-0.28.0-py37ha925a31_0 (this is a generated file);
print('===== testing package: llvmlite-0.28.0-py37ha925a31_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import os
from llvmlite.tests import main

# Enable tests for distribution only
os.environ['LLVMLITE_DIST_TEST'] = '1'
main()
#  --- run_test.py (end) ---

print('===== llvmlite-0.28.0-py37ha925a31_0 OK =====');
print("import: 'llvmlite'")
import llvmlite

print("import: 'llvmlite.binding'")
import llvmlite.binding

