



sqlite3 --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
IF NOT EXIST %LIBRARY_BIN%\sqlite3.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
IF NOT EXIST %LIBRARY_LIB%\sqlite3.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
IF NOT EXIST %LIBRARY_INC%\sqlite3.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
