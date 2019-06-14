



f2py -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -c "import numpy; numpy.show_config()"
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
