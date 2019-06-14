



if not exist %PREFIX%\\Library\\bin\\tiff.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\bin\\tiffxx.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\bin\\libtiff.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\bin\\libtiffxx.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
