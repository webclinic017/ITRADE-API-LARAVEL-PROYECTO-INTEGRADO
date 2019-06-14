#!C:\ci\conda-verify_1538577409397\_h_env\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'conda-verify==3.1.1','console_scripts','conda-verify'
__requires__ = 'conda-verify==3.1.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('conda-verify==3.1.1', 'console_scripts', 'conda-verify')()
    )
