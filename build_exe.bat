@echo off
setlocal
title 打包 MODELER 汉化工具

echo ============================================================
echo   打包 exe
echo ============================================================
echo.

cd /d "%~dp0"

set "PY="
for %%p in (py python python3) do (
    if not defined PY (
        %%p --version >nul 2>&1
        if not errorlevel 1 set "PY=%%p"
    )
)

if not defined PY (
    echo [错误] 需要 Python。
    pause
    exit /b 1
)

echo 清理旧产物...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist MODELER-ZH.spec del /q MODELER-ZH.spec

echo.
echo 开始打包（可能需要几分钟）...
echo.

%PY% -m PyInstaller ^
    --onefile ^
    --console ^
    --name "MODELER-ZH" ^
    --add-data "tools\data;data" ^
    --paths tools ^
    --noconfirm ^
    --clean ^
    tools\exe_entry.py

if errorlevel 1 (
    echo.
    echo [失败] 打包出错。
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   完成
echo.
echo   产物：dist\MODELER-ZH.exe
echo.
if exist "dist\MODELER-ZH.exe" (
    for %%f in ("dist\MODELER-ZH.exe") do echo   大小：%%~zf 字节
)
echo ============================================================
echo.
pause
