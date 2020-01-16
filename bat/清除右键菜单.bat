@echo off
cd /d "%~dp0"
Rd "%WinDir%\system32\test_permissions" >NUL 2>NUL
Md "%WinDir%\System32\test_permissions" 2>NUL||(Echo 请使用右键管理员身份运行！&&Pause >nul&&Exit)
Rd "%WinDir%\System32\test_permissions" 2>NUL

reg delete "HKEY_CLASSES_ROOT\*\shell\PartExtract-bat" /f
ping 127.0.0.1 -n 3 >nul 
