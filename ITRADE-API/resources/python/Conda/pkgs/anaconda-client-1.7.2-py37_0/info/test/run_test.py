#  tests for anaconda-client-1.7.2-py37_0 (this is a generated file);
print('===== testing package: anaconda-client-1.7.2-py37_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import binstar_client

print('binstar_client.__version__: %s' % binstar_client.__version__)
assert binstar_client.__version__.startswith('1.7.2')
#  --- run_test.py (end) ---

print('===== anaconda-client-1.7.2-py37_0 OK =====');
print("import: 'binstar_client'")
import binstar_client

print("import: 'binstar_client.scripts.cli'")
import binstar_client.scripts.cli

