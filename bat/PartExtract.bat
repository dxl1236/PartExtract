@echo off
color 3E
title NXװ����ȡ���
cd /d "%~dp0"
if NOT EXIST "%~dp07z.exe" echo.���߲�������û�ҵ�7z.exe��&&pause>nul&&exit 
if NOT EXIST "%~dp0ugpc.exe" echo.���߲�������û�ҵ�ugpc.exe��&&pause>nul&&exit 
echo.ѡ����ļ�Ϊ��"%~nx1"
ugpc %1 1>nul 2>nul
if %errorlevel%==0 (
goto asm
) else if %errorlevel%==4 (
echo.ѡ���"%~nx1"�ļ�����װ���ļ�!
set "msgvar=ѡ���%~nx1�ļ�����װ���ļ�!"
goto msg
) else if %errorlevel%==5 (
echo.ѡ���prt�ļ��汾����!
set "msgvar=ѡ���%~nx1�ļ��汾����!"
goto msg
) else if %errorlevel%==9009 (
echo.���߰�װ������,���޸�!
set "msgvar=���߰�װ������,���޸�!"
goto msg
) else ( echo.ѡ���"%~nx1"�ļ�����NX prt�ļ�!
set "msgvar=ѡ���%~nx1�ļ�����NX prt�ļ�!"
goto msg )
exit
:asm
Setlocal enabledelayedexpansion
set count1=0
set count2=0
set count3=0
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
set "file=%~n1-%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%%time:~6,2%%time:~9,2%"
) else (
set "file=%file%-%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%%time:~6,2%%time:~9,2%"
set "pack=%~dp1"
set "pack=!pack:~0,-1!.ack"
for /f "delims=" %%i in ("!pack!") do (
set uppath=%%~dpi
))

echo �½�Ŀ¼��"%uppath%\%file%\"
md "%uppath%\%file%\"
echo.���ڸ����ļ�...
echo.
echo.������������������������������������������������������������
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
if EXIST "%~dp1%%~nxi" ( 
xcopy /h /y /q "%~dp1%%~nxi" "%uppath%\%file%\" >nul
set /a count1+=1
) else if EXIST "%%i" ( 
xcopy /h /y /q "%%i" "%uppath%\%file%\" >nul
set /a count1+=1
set /a count3+=1
echo.  ��ǰĿ¼ȱʧ"%%~nxi"�����ϴα���Ŀ¼"%%~dpi"���ҵ������ʵ�汾.
) else ( echo. "%%~nxi"δ�ҵ������飡�� )
)
del /f list.txt
del /f error.txt
set /a count=%count2%-%count1%
echo.
echo.    ��%count2%���ļ�,����%count1%���ļ�,ȱ��%count%���ļ���
echo.
echo.������������������������������������������������������������
echo.
if %count%==0 (
echo.
echo.Ŀ¼�ļ�����,�����Ҫ����ļ��밴���������������رճ���&&pause>nul
goto upack
) else (
echo.
echo.###��ǰĿ¼�ļ���������ȱ��%count%���ļ��������������ȡ###
echo.
echo.�����Ҫǿ�ƴ���ļ��밴���������������رճ���&&pause>nul
goto upack
)
exit

:upack
cls
echo.
echo.���ڴ���ļ�...
if EXIST "%uppath%\%file%.7z" ( del /f  /q "%uppath%\%file%.7z" )
7z.exe  a  "%uppath%\%file%.7z"  "%uppath%\%file%\" 
)
echo.
echo.�����ɡ�
set msgvar=�����ɡ�
echo.
echo.�����Ҫɾ��Ŀ¼�밴���������������رճ���&&pause>nul
rd /s /q "%uppath%\%file%\"
echo.Ŀ¼ɾ����ɡ�
ping 127.0.0.1 -n 2 >nul 
exit

:msg
mshta vbscript:msgbox("%msgvar%",64,"��ʾ")(window.close) 
ping 127.0.0.1 -n 2 >nul 
exit







