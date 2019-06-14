



pt2to3 -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
ptdump -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
ptrepack -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
pttree -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
