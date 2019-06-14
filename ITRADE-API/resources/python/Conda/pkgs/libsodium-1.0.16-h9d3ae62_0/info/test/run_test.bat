



if not exist %LIBRARY_INC%\sodium.h              exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_INC%\sodium\version.h      exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_BIN%\libsodium.dll         exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_LIB%\libsodium.lib         exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %LIBRARY_LIB%\libsodium_static.lib  exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
exit 0
