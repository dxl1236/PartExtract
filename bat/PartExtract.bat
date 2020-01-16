@echo off
color 3E
title NX装配树提取打包
cd /d "%~dp0"
if NOT EXIST "%~dp07z.exe" echo.工具不完整，没找到7z.exe！&&pause>nul&&exit 
if NOT EXIST "%~dp0ugpc.exe" echo.工具不完整，没找到ugpc.exe！&&pause>nul&&exit 
echo.选择的文件为："%~nx1"
ugpc %1 1>nul 2>nul
if %errorlevel%==0 (
goto asm
) else if %errorlevel%==4 (
echo.选择的"%~nx1"文件不是装配文件!
set "msgvar=选择的%~nx1文件不是装配文件!"
goto msg
) else if %errorlevel%==5 (
echo.选择的prt文件版本过高!
set "msgvar=选择的%~nx1文件版本过高!"
goto msg
) else if %errorlevel%==9009 (
echo.工具安装有问题,请修复!
set "msgvar=工具安装有问题,请修复!"
goto msg
) else ( echo.选择的"%~nx1"文件不是NX prt文件!
set "msgvar=选择的%~nx1文件不是NX prt文件!"
goto msg )
exit
:asm
Setlocal enabledelayedexpansion
set count1=0
set count2=0
set var=%~dp1
:loop
for /f "delims=\  tokens=1*" %%i in ("%var%") do (
set file=%%i
set var=%%j
)
if defined var ( goto loop )
echo.%file%|find ":">nul
if %errorlevel%==0 (
set "uppath=%file%"
set "file=%~n1-%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%"
) else (
set "file=%file%-%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%"
set "pack=%~dp1"
set "pack=!pack:~0,-1!.ack"
for /f "delims=" %%i in ("!pack!") do (
set uppath=%%~dpi
))

echo 新建目录："%uppath%\%file%\"
md "%uppath%\%file%\"
echo.正在复制文件...
echo.
echo.┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
echo.
ugpc %1 1>nul 2>error.txt
echo.>list.txt
for /F "delims=" %%i in ('findstr /i  "not found" error.txt ') do (
set var=%%i
set vara=!var:~5,-10!
echo.!vara!>>list.txt
) 
ugpc %1 1>>list.txt 2>nul
for /F "delims=" %%i in (list.txt) do (
set /a count2+=1
if EXIST "%%i" ( 
xcopy /h /y /q "%%i" "%uppath%\%file%\" >nul
set /a count1+=1
) else ( echo. "%%~nxi"未找到，请检查！！ )
)
del /f list.txt
del /f error.txt
set /a count=%count2%-%count1%
echo.
echo.    共%count2%个文件,复制%count1%个文件,缺少%count%个文件。
echo.
echo.┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
echo.
if %count%==0 (
echo.
echo.目录文件完整,如果需要打包文件请按任意键继续，否则关闭程序！&&pause>nul
goto upack
) else (
echo.
echo.###当前目录文件不完整，缺少%count%个文件，请检查后重新提取###
echo.
echo.如果需要强制打包文件请按任意键继续，否则关闭程序！&&pause>nul
goto upack
)
exit

:upack
cls
echo.
echo.正在打包文件...
if EXIST "%uppath%\%file%.7z" ( del /f  /q "%uppath%\%file%.7z" )
7z.exe  a  "%uppath%\%file%.7z"  "%uppath%\%file%\" 
)
echo.
echo.打包完成。
set msgvar=打包完成。
echo.
echo.如果需要删除目录请按任意键继续，否则关闭程序！&&pause>nul
rd /s /q "%uppath%\%file%\"
echo.目录删除完成。
ping 127.0.0.1 -n 2 >nul 
exit

:msg
mshta vbscript:msgbox("%msgvar%",64,"提示")(window.close) 
ping 127.0.0.1 -n 2 >nul 
exit







