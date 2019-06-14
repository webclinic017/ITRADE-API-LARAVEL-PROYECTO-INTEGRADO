



if exist %LIBRARY_BIN%\freetype.dll (exit 0) else (exit 1)
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
