# Regenerates all SVG graphics and renders them to PNG (resvg, Arial).
$root = Split-Path $PSScriptRoot -Parent
$resvg = "C:\Repos\resvg.exe"
python (Join-Path $PSScriptRoot "gen_tiles.py")
python (Join-Path $PSScriptRoot "gen_graphics.py")
$jobs = @(
  @("Installer\store\cover", 1200), @("docs\hero_ruler", 1000), @("docs\hero_dial", 640),
  @("docs\protractor", 800), @("docs\workflow", 1000), @("docs\move_sequence", 900))
foreach ($j in $jobs) {
  & $resvg --width $j[1] --font-family Arial --sans-serif-family Arial `
    (Join-Path $root "$($j[0]).svg") (Join-Path $root "$($j[0]).png")
}

# tile-style icons and the app logo (docs/tiles)
Get-ChildItem (Join-Path $PSScriptRoot "tiles") -Filter tile_*.svg | ForEach-Object {
  & $resvg --width 256 $_.FullName ($_.FullName -replace '\.svg$', '.png')
}
& $resvg --width 128 (Join-Path $PSScriptRoot "tiles\tile_logo.svg") (Join-Path $PSScriptRoot "tiles\tile_logo_128.png")
& $resvg (Join-Path $PSScriptRoot "tiles\contact_sheet.svg") (Join-Path $PSScriptRoot "tiles\contact_sheet.png")
