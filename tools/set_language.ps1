# Set MODELER language id to chinese_tc
# Called by the one-click cmd with administrator privileges.
# IMPORTANT: keep this file pure ASCII.
#   powershell.exe reads .ps1 as ANSI on this system; non-ASCII comments
#   can swallow the following newline and break the script.
#
# Safety: [System.IO.File]::WriteAllText truncates the target before writing,
#   so a rejected write would leave a 0-byte file.
#   Use: write temp -> verify -> remove target -> move temp, restore on failure.

$ErrorActionPreference = 'Stop'

$Target = $env:ProgramData + '\CELSYS\CLIPStudio\InstallPath\modeler15.txt'
$ResultFile = $env:TEMP + '\modeler_setlang_result.txt'

function Finish($code, $message) {
    Write-Host ''
    if ($code -eq 0) {
        Write-Host $message -ForegroundColor Green
    }
    else {
        Write-Host $message -ForegroundColor Red
    }
    Write-Host ''
    try {
        Set-Content -LiteralPath $ResultFile -Value $message -Encoding UTF8 -ErrorAction SilentlyContinue
    }
    catch { }
    Start-Sleep -Seconds 2
    exit $code
}

Write-Host '========================================'
Write-Host ' Set MODELER language to chinese_tc'
Write-Host '========================================'
Write-Host ''

if (-not (Test-Path -LiteralPath $Target)) {
    Finish 1 ('ERROR: file not found - ' + $Target)
}

$Backup = $Target + '.bak'
$Temp = $Target + '.new'

# ---------- step 1: read current content ----------
$original = [System.IO.File]::ReadAllText($Target)

if ($original.Length -lt 20) {
    # target looks broken, try backup
    if (Test-Path -LiteralPath $Backup) {
        Write-Host 'target looks broken, reading from backup...' -ForegroundColor Yellow
        $original = [System.IO.File]::ReadAllText($Backup)
    }
    else {
        Finish 1 'ERROR: target is empty and no backup available'
    }
}
else {
    # refresh backup with current good content
    try {
        [System.IO.File]::WriteAllText($Backup, $original)
    }
    catch {
        Write-Host 'WARN: could not refresh backup' -ForegroundColor Yellow
    }
}

Write-Host 'BEFORE:'
Write-Host $original

if ($original -match '"Language"\s*=\s*"chinese_tc"') {
    Finish 0 'ALREADY: language is already chinese_tc'
}

# ---------- step 2: build new content ----------
$new = [regex]::Replace($original, '"Language"\s*=\s*"[^"]*"', '"Language"="chinese_tc"')

if ($new -eq $original) {
    Finish 1 'ERROR: Language line not found, file untouched'
}

if ($new -notmatch 'AppPath15') {
    Finish 1 'ERROR: result looks invalid, aborted'
}

# ---------- step 3: write temp and verify ----------
try {
    [System.IO.File]::WriteAllText($Temp, $new, [System.Text.Encoding]::UTF8)
}
catch {
    Finish 1 ('ERROR: write temp failed - ' + $_.Exception.Message)
}

$verify = [System.IO.File]::ReadAllText($Temp)

if ($verify -ne $new) {
    Remove-Item -LiteralPath $Temp -Force -ErrorAction SilentlyContinue
    Finish 1 'ERROR: temp file verification failed'
}

# ---------- step 4: replace ----------
try {
    Remove-Item -LiteralPath $Target -Force -ErrorAction Stop
    Move-Item -LiteralPath $Temp -Destination $Target -Force -ErrorAction Stop
}
catch {
    Write-Host ('replace failed: ' + $_.Exception.Message) -ForegroundColor Red
    try {
        if (Test-Path -LiteralPath $Backup) {
            Copy-Item -LiteralPath $Backup -Destination $Target -Force
            Write-Host 'restored from backup' -ForegroundColor Yellow
        }
    }
    catch { }
    Remove-Item -LiteralPath $Temp -Force -ErrorAction SilentlyContinue
    Finish 1 'ERROR: replace failed, backup restored'
}

# ---------- step 5: final check ----------
$final = [System.IO.File]::ReadAllText($Target)

Write-Host ''
Write-Host 'AFTER:'
Write-Host $final

if (($final -match '"Language"\s*=\s*"chinese_tc"') -and ($final.Length -gt 20)) {
    Finish 0 'OK: language changed to chinese_tc'
}
else {
    Finish 1 'ERROR: final check failed'
}
