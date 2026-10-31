@echo off
setlocal EnableExtensions DisableDelayedExpansion
title Homework 1 - Compile PDFs

echo Compiling the Chinese and English PDFs. Please wait...
echo.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"
set "taskCompileExitCode=%ERRORLEVEL%"

echo.
if "%taskCompileExitCode%"=="0" (
    echo SUCCESS: Both PDFs have been updated in this folder.
) else (
    echo FAILED: Read the error details above, fix the source, and try again.
)

if /I not "%~1"=="--no-pause" pause
exit /b %taskCompileExitCode%
