@echo off
setlocal

set "AHK=%LOCALAPPDATA%\Programs\AutoHotkey\v2\AutoHotkey64.exe"
if not exist "%AHK%" set "AHK=%ProgramFiles%\AutoHotkey\v2\AutoHotkey64.exe"

if not exist "%AHK%" (
    echo AutoHotkey v2 not found. Install via: winget install --id AutoHotkey.AutoHotkey -e
    pause
    exit /b 1
)

start "" "%AHK%" "%~dp0src\TextTransformer.ahk"
endlocal
