@echo off

for /f "usebackq delims=" %%a in (`powershell -NoProfile -Command ^
    "(Get-CimInstance -ClassName Win32_SystemEnclosure).ChassisTypes[0]"`) do set "CHASSIS=%%a"

set "DEVICE_TYPE=PC"
for %%a in (8 9 10 11 12 13 14 18 21 30 31 32) do if "%CHASSIS%"=="%%a" set "DEVICE_TYPE=LAPTOP"

if /I "%DEVICE_TYPE%"=="LAPTOP" (
	reg add "HKLM\SYSTEM\CurrentControlSet\Services\DisplayEnhancementService" /v Start /t REG_DWORD /d 3 /f
	reg add "HKLM\SYSTEM\CurrentControlSet\Services\acpiex" /v Start /t REG_DWORD /d 0 /f
    cls
)