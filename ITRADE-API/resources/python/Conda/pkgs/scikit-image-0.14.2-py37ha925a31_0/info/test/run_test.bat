



setx MPLBACKEND "Agg"
IF %ERRORLEVEL% NEQ 0 exit /B 1
pytest --pyargs skimage
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
