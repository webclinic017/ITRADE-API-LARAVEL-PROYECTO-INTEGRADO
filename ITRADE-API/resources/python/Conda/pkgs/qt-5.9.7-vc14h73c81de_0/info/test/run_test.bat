pushd test
if exist .qmake.stash del /a .qmake.stash
qmake hello.pro
if %ErrorLevel% neq 0 exit /b 1
nmake
if %ErrorLevel% neq 0 exit /b 1
:: Only test that this builds
nmake clean
if %ErrorLevel% neq 0 exit /b 1
qmake qtwebengine.pro
if %ErrorLevel% neq 0 exit /b 1
nmake
if %ErrorLevel% neq 0 exit /b 1
popd




if not exist %LIBRARY_BIN%\\Qt5WebEngine_conda.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %LIBRARY_PREFIX%\plugins\sqldrivers\qsqlite.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
