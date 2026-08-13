@echo off

for /f "usebackq delims=" %%a in (`powershell -NoProfile -Command ^
    "(Get-CimInstance -ClassName Win32_SystemEnclosure).ChassisTypes[0]"`) do set "CHASSIS=%%a"

set "DEVICE_TYPE=PC"
for %%a in (8 9 10 11 12 13 14 18 21 30 31 32) do if "%CHASSIS%"=="%%a" set "DEVICE_TYPE=LAPTOP"

if /I "%DEVICE_TYPE%"=="LAPTOP" (
    powercfg /setactive d90bd747-9a4a-44ac-b19a-661a723534f5
    powercfg /setacvalueindex scheme_current 54533251-82be-4824-96c1-47b60b740d00 4d2b0152-7d5c-498b-88e2-34345392a2c5 5000
    powercfg /setdcvalueindex scheme_current 54533251-82be-4824-96c1-47b60b740d00 4d2b0152-7d5c-498b-88e2-34345392a2c5 5000
    cls
) else (
    powercfg -import %SYSTEMROOT%\AkariOS.pow d90bd747-9a4a-44ac-b19a-661a723534f5
    powercfg -setactive d90bd747-9a4a-44ac-b19a-661a723534f5 
    del %SYSTEMROOT%\AkariOS.pow
    cls
)