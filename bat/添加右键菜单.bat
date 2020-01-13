@echo off

Rd "%WinDir%\system32\test_permissions" >NUL 2>NUL
Md "%WinDir%\System32\test_permissions" 2>NUL||(Echo 请使用右键管理员身份运行！&&Pause >nul&&Exit)
Rd "%WinDir%\System32\test_permissions" 2>NUL
cd /d "%~dp0"
if NOT EXIST "%~dp0ugraf.exe" echo.请放到UGII目录后再运行！&&pause>nul&&exit 
if NOT EXIST "%~dp0PartExtract.bat" echo.工具不完整，没找到PartExtract.bat！&&pause>nul&&exit 
if NOT EXIST "%~dp07z.exe" echo.工具不完整，没找到7z.exe！&&pause>nul&&exit 
if NOT EXIST "%~dp0ugpc.exe" echo.工具不完整，没找到ugpc.exe！&&pause>nul&&exit 
reg delete "HKEY_CLASSES_ROOT\*\shell\PartExtract" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PartExtract"   /d "NX装配提取打包" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PartExtract\command"   /d "%~dp0PartExtract.bat  \"%%1\""  /f
ping 127.0.0.1 -n 3 >nul 