@echo off
setlocal
set "DIR=%~dp0"
set "ARCH=amd64"
if /I "%PROCESSOR_ARCHITECTURE%"=="ARM64" set "ARCH=arm64"
if /I "%PROCESSOR_ARCHITEW6432%"=="ARM64" set "ARCH=arm64"
set "BIN=%DIR%bin\statussvc-windows-%ARCH%.exe"
if not exist "%BIN%" (
  echo No binary at %BIN% — available:
  dir /B "%DIR%bin"
  exit /b 1
)
"%BIN%" %*
