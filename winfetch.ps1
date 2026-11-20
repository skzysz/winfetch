$esc = [char]27

# Читаем системный акцентный цвет из реестра (DWM)
$accentColor = 0
try {
    $regKey = Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\DWM" -Name "ColorizationColor" -ErrorAction Stop
    $accentColor = $regKey.ColorizationColor
} catch {
    $accentColor = 0xCC000000 # fallback — синий
}

# Разбираем DWORD (0xAARRGGBB) на R, G, B
$b = ($accentColor -shr 16) -band 0xFF
$g = ($accentColor -shr 8) -band 0xFF
$r = $accentColor -band 0xFF

# Формируем ANSI-код для акцентного цвета
$accentAnsi = "$esc[38;2;$r;$g;${b}m"
$white = "$esc[97m"
$reset = "$esc[0m"

$packages = "Unknown"
try {
    $wingetList = winget list 2>$null
    if ($wingetList) {
        $count = ($wingetList | Measure-Object -Line).Lines - 3
        $packages = "$count (winget)"
    }
} catch { }

$refresh = "Unknown"
try {
    $rRate = (Get-CimInstance Win32_VideoController | Select-Object -First 1).CurrentRefreshRate
    if ($rRate) { $refresh = "$rRate Hz" }
} catch { }

Write-Host "$accentAnsi Packages: $reset$white$packages$reset"
Write-Host "$accentAnsi Refresh:  $reset$white$refresh$reset"

# Палитра цветов — тоже в оттенках акцента (или стандартная)
$palette = "$esc[40m  $esc[41m  $esc[42m  $esc[43m  $esc[44m  $esc[45m  $esc[46m  $esc[47m  $esc[0m"
Write-Host ""
Write-Host $palette