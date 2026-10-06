# Regenerates all icons: python gen_icons.py (SVG) then resvg (PNG, 64 px). Run from any folder.
$dir = $PSScriptRoot
$resvg = "C:\Repos\resvg.exe"
if (Get-Command python -ErrorAction SilentlyContinue) { Push-Location $dir; python gen_icons.py; Pop-Location }
Get-ChildItem $dir -Filter *.svg | ForEach-Object {
    $png = [IO.Path]::ChangeExtension($_.FullName, ".png")
    & $resvg --width 64 $_.FullName $png
}
Write-Host "rendered" (Get-ChildItem $dir -Filter *.png).Count "icons"
