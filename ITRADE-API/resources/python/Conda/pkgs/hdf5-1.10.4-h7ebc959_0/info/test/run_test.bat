



where gif2h5
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h52gif
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5copy
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5debug
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5diff
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5dump
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5import
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5jam
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5ls
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5mkgrp
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5repack
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5repart
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5stat
IF %ERRORLEVEL% NEQ 0 exit /B 1
where h5unjam
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\lib\\hdf5.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\bin\\hdf5.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\lib\\hdf5_cpp.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\bin\\hdf5_cpp.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\lib\\hdf5_hl.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\bin\\hdf5_hl.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\lib\\hdf5_hl_cpp.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\\bin\\hdf5_hl_cpp.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
