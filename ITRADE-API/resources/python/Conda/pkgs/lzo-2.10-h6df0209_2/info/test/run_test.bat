



if not exist %PREFIX%\\Library\\include\\lzo\\lzoconf.h exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %PREFIX%\\Library\\lib\\lzo2.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %PREFIX%\\Library\\lib\\lzo2_dllimport.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
if not exist %PREFIX%\\Library\\bin\\lzo2.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit 1
exit 0
