



if exist %LIBRARY_LIB%\libzmq-mt-s-4_3_1.lib (exit 0) else (exit 1)
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_BIN%\libzmq-mt-4_3_1.dll (exit 0) else (exit 1)
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_LIB%\libzmq-mt-4_3_1.lib (exit 0) else (exit 1)
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_BIN%\libzmq.dll (exit 0) else (exit 1)
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_LIB%\libzmq.lib (exit 0) else (exit 1)
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_PREFIX%\cmake\ZeroMQ\ZeroMQConfig.cmake (exit 0) else (exit 1)
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %LIBRARY_PREFIX%\cmake\ZeroMQ\ZeroMQConfigVersion.cmake (exit 0) else (exit 1)
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
