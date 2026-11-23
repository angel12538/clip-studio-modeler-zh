@echo off
setlocal
title CLIP STUDIO MODELER 还原原版

echo ============================================================
echo   还原为英文原版
echo ============================================================
echo.
echo   请先完全退出 CLIP STUDIO MODELER。
echo.
pause

cd /d "%~dp0"

set "PY="
for %%p in (py python python3) do (
    if not defined PY (
        %%p --version >nul 2>&1
        if not errorlevel 1 set "PY=%%p"
    )
)

if not defined PY (
    echo.
    echo [错误] 没有找到 Python，无法自动还原。
    echo.
    echo 手动还原步骤：
    echo   1. 删除 MODELER 安装目录下的 resource\chinese_tc 文件夹
    echo   2. 把 %ProgramData%\CELSYS\CLIPStudio\InstallPath\modeler15.txt
    echo      中的 "Language" 改为 "english"
    echo.
    pause
    exit /b 1
)

echo.
echo ------------------------------------------------------------
echo   将要：
echo     1. 删除 resource\chinese_tc 目录
echo     2. 把材质标签改回英文
echo.
echo   语言标识需手动改回 english。
echo ------------------------------------------------------------
echo.
choice /C YN /M "  确认还原"
if errorlevel 2 (
    echo 已取消。
    pause
    exit /b 0
)

echo.
%PY% tools\rollback.py --apply

echo.
echo ------------------------------------------------------------
echo   材质标签已还原。语言标识请手动修改：
echo.
echo     用【管理员权限的记事本】打开
echo       %ProgramData%\CELSYS\CLIPStudio\InstallPath\modeler15.txt
echo     把 "Language"="chinese_tc" 改为 "Language"="english"
echo ------------------------------------------------------------
echo.
pause
