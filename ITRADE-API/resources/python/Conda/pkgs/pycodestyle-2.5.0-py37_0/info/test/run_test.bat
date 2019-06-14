



pycodestyle --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
pycodestyle --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
