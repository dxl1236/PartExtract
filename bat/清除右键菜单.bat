@echo off
cd /d "%~dp0"
Rd "%WinDir%\system32\test_permissions" >NUL 2>NUL
Md "%WinDir%\System32\test_permissions" 2>NUL||(Echo ��ʹ���Ҽ�����Ա������У�&&Pause >nul&&Exit)
Rd "%WinDir%\System32\test_permissions" 2>NUL

reg delete "HKEY_CLASSES_ROOT\*\shell\PartExtract" /f
ping 127.0.0.1 -n 3 >nul 