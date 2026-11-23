# 把 modeler15.txt 的语言标识改为 chinese_tc
# 需要管理员权限运行（脚本会自动请求提权）
# 注意：本文件保持纯 ASCII，避免 Windows PowerShell 以 ANSI 读取时乱码

$ErrorActionPreference = 'Stop'

$Log = $env:TEMP + '\modeler_setlang.log'

function Log($m) {
    Add-Content -LiteralPath $Log -Value $m -Encoding UTF8 -ErrorAction SilentlyContinue
}

Set-Content -LiteralPath $Log -Value '' -Encoding UTF8 -ErrorAction SilentlyContinue

$Target = $env:ProgramData + '\CELSYS\CLIPStudio\InstallPath\modeler15.txt'

Log "=== modeler language switch ==="
Log "target: $Target"

if (-not (Test-Path -LiteralPath $Target)) {
    Log "ERROR: target not found"
    Write-Host "错误：找不到 $Target" -ForegroundColor Red
    Write-Host "请先运行一次 CLIP STUDIO MODELER 生成配置。" -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    exit 1
}

# 备份
$Backup = $Target + '.bak'
if (-not (Test-Path -LiteralPath $Backup)) {
    Copy-Item -LiteralPath $Target -Destination $Backup -Force
    Log "backup created: $Backup"
}

$text = [System.IO.File]::ReadAllText($Target)
Log ("before: " + $text.Replace("`r`n", ' | '))

if ($text -match 'chinese_tc') {
    Write-Host "语言标识已经是 chinese_tc，无需修改。" -ForegroundColor Green
    Log "already chinese_tc"
}
else {
    $new = $text -replace '"Language"\s*=\s*"[^"]*"', '"Language"="chinese_tc"'
    if ($new -eq $text) {
        Write-Host "警告：未找到 Language 行，未做修改。" -ForegroundColor Yellow
        Log "WARN: Language line not found"
    }
    else {
        [System.IO.File]::WriteAllText($Target, $new)
        Write-Host "已改为 chinese_tc" -ForegroundColor Green
        Log "changed to chinese_tc"
    }
}

$after = [System.IO.File]::ReadAllText($Target)
Log ("after: " + $after.Replace("`r`n", ' | '))
Write-Host ""
Write-Host "当前内容：" -ForegroundColor Cyan
Write-Host $after
Log "done"
