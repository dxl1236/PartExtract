@echo off

Rd "%WinDir%\system32\test_permissions" >NUL 2>NUL
Md "%WinDir%\System32\test_permissions" 2>NUL||(Echo ��ʹ���Ҽ�����Ա������У�&&Pause >nul&&Exit)
Rd "%WinDir%\System32\test_permissions" 2>NUL
cd /d "%~dp0"
if NOT EXIST "%~dp0ugraf.exe" echo.��ŵ�UGIIĿ¼�������У�&&pause>nul&&exit 
if NOT EXIST "%~dp0PartExtract.bat" echo.���߲�������û�ҵ�PartExtract.bat��&&pause>nul&&exit 
if NOT EXIST "%~dp07z.exe" echo.���߲�������û�ҵ�7z.exe��&&pause>nul&&exit 
if NOT EXIST "%~dp0ugpc.exe" echo.���߲�������û�ҵ�ugpc.exe��&&pause>nul&&exit 
reg delete "HKEY_CLASSES_ROOT\*\shell\PartExtract" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PartExtract"   /d "NXװ����ȡ���" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PartExtract\command"   /d "%~dp0PartExtract.bat  \"%%1\""  /f
ping 127.0.0.1 -n 3 >nul 