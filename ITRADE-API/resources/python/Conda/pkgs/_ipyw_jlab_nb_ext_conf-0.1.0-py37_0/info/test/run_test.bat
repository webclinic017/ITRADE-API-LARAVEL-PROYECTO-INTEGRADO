



jupyter-nbextension list
IF %ERRORLEVEL% NEQ 0 exit /B 1
jupyter-serverextension list
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
