



dask-scheduler --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
dask-ssh --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
dask-worker --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
