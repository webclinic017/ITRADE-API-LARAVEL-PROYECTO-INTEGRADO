



if not exist %LIBRARY_INC%\snappy.h exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_INC%\snappy-stubs-public.h exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_LIB%\snappy.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_BIN%\snappy.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_LIB%\snappy_static.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
exit 0
