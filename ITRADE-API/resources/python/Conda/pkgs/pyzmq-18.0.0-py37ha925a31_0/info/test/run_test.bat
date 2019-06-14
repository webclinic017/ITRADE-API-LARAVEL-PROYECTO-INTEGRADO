



py.test --pyargs zmq.tests.test_socket
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
