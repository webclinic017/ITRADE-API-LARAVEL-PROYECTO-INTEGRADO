



IF NOT EXIST %SP_DIR%\numpy\distutils\site.cfg exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
