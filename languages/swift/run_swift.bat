@echo off
REM Swift wrapper for Windows - compiles and runs the gladiator.swift

set "SCRIPT=%~1"
set "SCRIPT_DIR=%~dp1"
set "EXE=%SCRIPT_DIR%gladiator.exe"

REM Check if executable is older than source or doesn't exist
if not exist "%EXE%" goto COMPILE
if "%SCRIPT%" neq "" if "%SCRIPT%" gtr "%EXE%" goto COMPILE

REM Run the executable
"%EXE%"
exit /b %errorlevel%

:COMPILE
swiftc "%SCRIPT%" -o "%EXE%"
if errorlevel 1 (
    echo Compilation failed
    exit /b 1
)
"%EXE%"
exit /b %errorlevel%