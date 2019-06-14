



curl --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
curl https://raw.githubusercontent.com/conda-forge/curl-feedstock/master/LICENSE
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
