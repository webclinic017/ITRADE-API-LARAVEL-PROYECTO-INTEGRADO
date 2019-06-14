



pylint --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
where epylint
IF %ERRORLEVEL% NEQ 0 exit /B 1
pyreverse --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
symilar --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
