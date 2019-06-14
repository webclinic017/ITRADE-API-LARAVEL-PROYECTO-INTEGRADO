



IF NOT EXIST %LIBRARY_INC%/blosc.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
IF NOT EXIST %LIBRARY_INC%/blosc-export.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
IF NOT EXIST %LIBRARY_BIN%/blosc.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
IF NOT EXIST %LIBRARY_LIB%/blosc.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
