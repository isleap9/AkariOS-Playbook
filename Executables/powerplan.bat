@echo off

for /f "usebackq delims=" %%a in (`powershell -NoProfile -Command ^
    "(Get-CimInstance -ClassName Win32_SystemEnclosure).ChassisTypes[0]"`) do set "CHASSIS=%%a"

set "DEVICE_TYPE=PC"
for %%a in (8 9 10 11 12 13 14 18 21 30 31 32) do if "%CHASSIS%"=="%%a" set "DEVICE_TYPE=LAPTOP"

if /I "%DEVICE_TYPE%"=="LAPTOP" (
    powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e
    powercfg /setacvalueindex scheme_current 54533251-82be-4824-96c1-47b60b740d00 4d2b0152-7d5c-498b-88e2-34345392a2c5 5000
    powercfg /setdcvalueindex scheme_current 54533251-82be-4824-96c1-47b60b740d00 4d2b0152-7d5c-498b-88e2-34345392a2c5 5000
    cls
) else (
    powercfg -import %SYSTEMROOT%\AkariOS.pow 8b1e6fbd-33a2-411c-9317-232e23154cf5
    powercfg -setactive 8b1e6fbd-33a2-411c-9317-232e23154cf5
    del %SYSTEMROOT%\AkariOS.pow
    cls
)