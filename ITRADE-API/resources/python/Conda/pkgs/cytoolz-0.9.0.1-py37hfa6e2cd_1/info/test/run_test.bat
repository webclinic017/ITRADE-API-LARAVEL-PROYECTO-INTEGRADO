



nosetests --with-doctest cytoolz
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
