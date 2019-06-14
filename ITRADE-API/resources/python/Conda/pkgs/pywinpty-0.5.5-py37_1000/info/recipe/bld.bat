if "%ARCH%" == "32" (set PLATFORM=x86) else (set PLATFORM=x64)
"%PYTHON%" -m pip install . --no-deps --ignore-installed --no-cache-dir -vvv
if errorlevel 1 exit 1
