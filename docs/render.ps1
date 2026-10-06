# Regenerates all SVG graphics and renders them to PNG (resvg, Arial).
$root = Split-Path $PSScriptRoot -Parent
$resvg = "C:\Repos\resvg.exe"
python (Join-Path $PSScriptRoot "gen_graphics.py")
$jobs = @(
  @("Installer\store\cover", 1200), @("docs\hero_ruler", 1000), @("docs\hero_dial", 640),
  @("docs\protractor", 800), @("docs\workflow", 1000), @("docs\move_sequence", 900))
foreach ($j in $jobs) {
  & $resvg --width $j[1] --font-family Arial --sans-serif-family Arial `
    (Join-Path $root "$($j[0]).svg") (Join-Path $root "$($j[0]).png")
}
