



anaconda -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
anaconda --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
