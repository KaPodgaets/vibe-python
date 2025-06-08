@echo off
SETLOCAL

SET PID_FILE="vibe_python.pid"

IF EXIST %PID_FILE% (
    SET /p PID=< %PID_FILE%
    echo Stopping process with PID: %PID%
    taskkill /F /PID %PID%
    del %PID_FILE%
) ELSE (
    echo PID file not found. Process may not be running.
)

echo Starting new service instance...
start "VibePythonRPA" vibe-python start-service 