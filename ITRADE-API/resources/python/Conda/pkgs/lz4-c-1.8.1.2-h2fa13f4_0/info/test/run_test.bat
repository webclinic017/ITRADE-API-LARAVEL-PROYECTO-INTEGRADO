



echo on
IF %ERRORLEVEL% NEQ 0 exit 1
echo %CD%
IF %ERRORLEVEL% NEQ 0 exit 1
lz4 -h
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_INC%\\lz4.h exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_INC%\\lz4hc.h exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_INC%\\lz4frame.h exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_BIN%\\liblz4.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_LIB%\\liblz4.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_LIB%\\liblz4_static.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
exit 0
