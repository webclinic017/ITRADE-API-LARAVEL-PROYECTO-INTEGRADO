



SET CONDA_SHLVL=
IF %ERRORLEVEL% NEQ 0 exit /B 1
CALL %PREFIX%\condabin\conda_hook.bat
IF %ERRORLEVEL% NEQ 0 exit /B 1
CALL conda.bat activate base
IF %ERRORLEVEL% NEQ 0 exit /B 1
FOR /F "delims=" %%i IN ('python -c "import sys; print(sys.version_info[0])"') DO set "PYTHON_MAJOR_VERSION=%%i"
IF %ERRORLEVEL% NEQ 0 exit /B 1
set TEST_PLATFORM=win
IF %ERRORLEVEL% NEQ 0 exit /B 1
FOR /F "delims=" %%i IN ('python -c "import random as r; print(r.randint(0,4294967296))"') DO set "PYTHONHASHSEED=%%i"
IF %ERRORLEVEL% NEQ 0 exit /B 1
set
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda info || exit /b
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda create -y -p .\built-conda-test-env || exit /b
IF %ERRORLEVEL% NEQ 0 exit /B 1
CALL conda.bat activate .\built-conda-test-env || exit /b
IF %ERRORLEVEL% NEQ 0 exit /B 1
echo %CONDA_PREFIX%
IF %ERRORLEVEL% NEQ 0 exit /B 1
IF NOT "%CONDA_PREFIX%"=="%CD%\built-conda-test-env" EXIT /B 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
CALL conda.bat deactivate || exit /b
IF %ERRORLEVEL% NEQ 0 exit /B 1
echo allow failures
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
