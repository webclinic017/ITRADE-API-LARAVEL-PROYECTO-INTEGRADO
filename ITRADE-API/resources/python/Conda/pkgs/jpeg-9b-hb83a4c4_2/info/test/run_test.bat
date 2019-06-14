



djpeg -dct int -ppm -outfile testout.ppm testorig.jpg
IF %ERRORLEVEL% NEQ 0 exit 1
exit 0
