# do not build winpty.exe as this requires a Cygwin/MSYS targetting toolchain
./configure
make build/winpty-agent.exe
make build/winpty.dll

# copy the necessary files
cp build/winpty-agent.exe ${LIBRARY_BIN}/winpty-agent.exe
cp build/winpty.dll ${LIBRARY_BIN}/winpty.dll
cp build/winpty.lib ${LIBRARY_LIB}/winpty.lib
cp src/include/* ${LIBRARY_INC}/
