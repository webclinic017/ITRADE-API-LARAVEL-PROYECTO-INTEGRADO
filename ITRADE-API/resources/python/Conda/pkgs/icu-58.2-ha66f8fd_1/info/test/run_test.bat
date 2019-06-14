



genbrk --help
IF %ERRORLEVEL% NEQ 0 exit 1
gencfu --help
IF %ERRORLEVEL% NEQ 0 exit 1
gencnval --help
IF %ERRORLEVEL% NEQ 0 exit 1
gendict --help
IF %ERRORLEVEL% NEQ 0 exit 1
icuinfo --help
IF %ERRORLEVEL% NEQ 0 exit 1
makeconv gb-18030-2000.ucm
IF %ERRORLEVEL% NEQ 0 exit 1
exit 0
