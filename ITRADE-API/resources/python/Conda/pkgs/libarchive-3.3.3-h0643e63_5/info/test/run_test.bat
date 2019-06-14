



bsdcat --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
bsdcpio --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
bsdtar --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
bsdtar -tf test/hello_world.xar
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
