



where conda-build
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda-build -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
where conda-convert
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda-convert -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
where conda-develop
IF %ERRORLEVEL% NEQ 0 exit /B 1
where conda-debug
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda-develop -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
where conda-index
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda-index -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
where conda-inspect
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda-inspect -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
where conda-metapackage
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda-metapackage -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
where conda-render
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda-render -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
where conda-skeleton
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda-skeleton -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
python test_bdist_conda_setup.py bdist_conda --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
