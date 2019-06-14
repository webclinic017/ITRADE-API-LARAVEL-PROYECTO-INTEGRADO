



xz --help
IF %ERRORLEVEL% NEQ 0 exit 1
unxz --help
IF %ERRORLEVEL% NEQ 0 exit 1
echo greetings > hello.txt
IF %ERRORLEVEL% NEQ 0 exit 1
xz -z hello.txt
IF %ERRORLEVEL% NEQ 0 exit 1
xz -d hello.txt.xz
IF %ERRORLEVEL% NEQ 0 exit 1
findstr greetings hello.txt && (exit /b 0) || (exit /b 1)
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %PREFIX%\\Library\\bin\\liblzma.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %PREFIX%\\Library\\lib\\liblzma.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %PREFIX%\\Library\\lib\\liblzma_static.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %PREFIX%\\Library\\include\\lzma.h exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
exit 0
