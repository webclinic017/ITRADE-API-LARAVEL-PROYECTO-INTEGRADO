if errorlevel 1 exit 1

COPY %PREFIX%\site.cfg site.cfg

python setup.py install --single-version-externally-managed --record=record.txt
if errorlevel 1 exit 1
