@echo off
setlocal enabledelayedexpansion
title CLIP STUDIO MODELER 简体中文汉化

echo ============================================================
echo   CLIP STUDIO MODELER 简体中文汉化
echo ============================================================
echo.
echo   请先完全退出 CLIP STUDIO MODELER（含托盘图标）。
echo.
pause

cd /d "%~dp0"

rem ========== 1. 检查 Python ==========
set "PY="
for %%p in (py python python3) do (
    if not defined PY (
        %%p --version >nul 2>&1
        if not errorlevel 1 set "PY=%%p"
    )
)

if not defined PY (
    echo.
    echo [错误] 没有找到 Python。
    echo.
    echo 请先安装 Python 3.8 或更高版本：
    echo     https://www.python.org/downloads/
    echo 安装时勾选 "Add Python to PATH"。
    echo.
    echo 或者下载 Release 里的 exe 版本，免安装 Python。
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('%PY% --version 2^>^&1') do set "PYVER=%%v"
echo [1/4] Python 已就绪  版本 %PYVER%
echo.

rem ========== 2. 检查 MODELER ==========
echo [2/4] 检查安装位置
echo.
%PY% tools\config.py
if errorlevel 1 (
    echo.
    echo 若上面显示"未找到"，请设置环境变量 MODELER_DIR 后重新运行：
    echo     set MODELER_DIR=^<MODELER 安装目录^>
    echo.
    pause
    exit /b 1
)
echo.

rem ========== 3. 语言标识 ==========
echo [3/4] 语言标识
echo.

set "CFG=%ProgramData%\CELSYS\CLIPStudio\InstallPath\modeler15.txt"
set "LANGOK=0"

if exist "%CFG%" (
    findstr /C:"chinese_tc" "%CFG%" >nul 2>&1
    if not errorlevel 1 set "LANGOK=1"
)

if "%LANGOK%"=="1" (
    echo   已经是 chinese_tc，无需修改。
    echo.
    goto dohack
)

echo   当前不是 chinese_tc，需要修改才能生效。
echo   文件：%CFG%
echo.
echo   这一步需要管理员权限。
echo.
choice /C YN /M "  现在自动修改"
if errorlevel 2 goto manual

echo.
echo   正在请求管理员权限...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-NoExit','-File','\"%~dp0tools\set_language.ps1\"' -Verb RunAs"
echo.
echo   请在弹出的窗口确认结果后，回到这里继续。
echo.
pause
goto dohack

:manual
echo.
echo   请手动修改：
echo     1. 用【管理员权限的记事本】打开
echo          %CFG%
echo     2. 把 "Language"="english" 改为 "Language"="chinese_tc"
echo     3. 保存后回到这里继续
echo.
pause

:dohack
echo [4/4] 生成中文资源
echo.
choice /C YN /M "  现在开始汉化"
if errorlevel 2 goto cancel

echo.
%PY% tools\apply_all.py --apply
if errorlevel 1 (
    echo.
    echo [失败] 请查看上方错误提示。
    pause
    exit /b 1
)

echo.
echo ------------------------------------------------------------
echo   资源已生成。是否同时汉化材质标签？
echo   标签存放在材质库中，需要单独处理。
echo ------------------------------------------------------------
choice /C YN /M "  汉化材质标签"
if errorlevel 2 goto finish

echo.
%PY% tools\apply_tags.py --apply

:finish
echo.
echo ============================================================
echo   完成！
echo.
echo   请启动 CLIP STUDIO MODELER 查看效果。
echo.
echo   若界面仍是英文：
echo     1. 检查 modeler15.txt 中 Language 是否为 chinese_tc
echo     2. 确认程序已完全重启
echo.
echo   要还原原版，运行：还原原版.cmd
echo ============================================================
echo.
pause
exit /b 0

:cancel
echo.
echo 已取消，未做任何修改。
pause
exit /b 0
