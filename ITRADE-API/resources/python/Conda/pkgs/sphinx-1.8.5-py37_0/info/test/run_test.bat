



sphinx-build -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
sphinx-quickstart --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
sphinx-quickstart -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
sphinx-apidoc -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
sphinx-autogen -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
