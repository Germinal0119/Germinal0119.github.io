<#
setup-project.ps1

Creates the consolidated project folder structure described in Section 1
of the plan, in one place, instead of scattered across C:\Users\nikala\...

Usage:
    1. Create/choose the ONE folder this whole project will live in, e.g.:
           mkdir C:\Users\nikala\Documents\illustration-archive
    2. Copy this script (and prep_batch.py, STAGES.md) into that folder.
    3. cd into that folder and run:
           .\setup-project.ps1
    4. Once you've confirmed the new structure looks right, delete the old
       scattered folders (the scripts\ one in Users\, the old _illustrations\
       in Users\, and the old illustrations folder in Documents) — this
       script does not touch them, so nothing is deleted automatically.
#>

$folders = @(
    "scripts",
    "data",
    "_illustrations",
    "assets\images\illustrations\full",
    "assets\images\illustrations\thumb",
    "illustrations-source",
    ".github\workflows"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    Write-Host "  created $folder"
}

if (-not (Test-Path "data\journals.yml")) {
    $journalTemplate = @'
# slug: "Georgian journal name"
# example:
# droeba: "დროება"
'@
    Set-Content -Path "data\journals.yml" -Value $journalTemplate -Encoding utf8
    Write-Host "  created data\journals.yml"
}

if (-not (Test-Path "data\tags.yml")) {
    Set-Content -Path "data\tags.yml" -Value "# canonical tag list, one per line, grows organically as you add batches`n" -Encoding utf8
    Write-Host "  created data\tags.yml"
}

if (-not (Test-Path ".gitignore")) {
    Set-Content -Path ".gitignore" -Value "_site/`npagefind/`n.jekyll-cache/`n" -Encoding utf8
    Write-Host "  created .gitignore"
}

Write-Host ""
Write-Host "Project structure created in $(Get-Location)"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Move prep_batch.py into .\scripts\"
Write-Host "  2. Add your first journal to data\journals.yml"
Write-Host "  3. git init, create the GitHub repo, and push once (even empty)"
Write-Host "  4. See STAGES.md for the full sequence"
