# Regenerates all icons: gen_icons.py and gen_headers.py (SVG), then resvg (PNG): 64 px icons, 360 px header images.
$dir = $PSScriptRoot
$resvg = "C:\Repos\resvg.exe"
if (Get-Command python -ErrorAction SilentlyContinue) {
    Push-Location $dir; python gen_icons.py; python gen_headers.py; Pop-Location
}
Get-ChildItem $dir -Filter *.svg | ForEach-Object {
    $width = 64
    if ($_.Name -like "header_*") { $width = 360 }
    & $resvg --width $width $_.FullName ([IO.Path]::ChangeExtension($_.FullName, ".png"))
}
Write-Host "rendered" (Get-ChildItem $dir -Filter *.png).Count "images"
