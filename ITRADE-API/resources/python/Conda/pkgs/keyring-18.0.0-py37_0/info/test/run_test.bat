



py.test -v keyring/tests
IF %ERRORLEVEL% NEQ 0 exit /B 1
keyring --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
