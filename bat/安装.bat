@echo off
Rd "%WinDir%\system32\test_permissions" >NUL 2>NUL
Md "%WinDir%\System32\test_permissions" 2>NUL||(Echo 请使用右键管理员身份运行！&&Pause >nul&&Exit)
Rd "%WinDir%\System32\test_permissions" 2>NUL
if EXIST "%UGII_ROOT_DIR%" (
xcopy /h /y /q "%~dp07z.exe" "%UGII_ROOT_DIR%"
xcopy /h /y /q "%~dp0PartExtract.bat"  "%UGII_ROOT_DIR%"
reg delete "HKEY_CLASSES_ROOT\*\shell\PartExtract-bat" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PartExtract-bat"   /d "NX装配树提取打包(bat)" /f
reg add "HKEY_CLASSES_ROOT\*\shell\PartExtract-bat\command"   /d "%UGII_ROOT_DIR%\PartExtract.bat  \"%%1\""  /f
echo.安装完成。
ping 127.0.0.1 -n 3 >nul 
) else echo.环境变量设置有问题，请手动复制所以文件到UGII目录后运行注册右键.bat！&&pause>nul&&exit 


