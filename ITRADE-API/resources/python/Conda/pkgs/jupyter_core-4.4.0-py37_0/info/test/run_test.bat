



jupyter -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
jupyter-migrate -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
jupyter-troubleshoot --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
