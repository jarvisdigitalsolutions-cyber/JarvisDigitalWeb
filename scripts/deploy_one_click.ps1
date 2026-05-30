<#
One-click deploy script (PowerShell)
Usage examples:
  .\deploy_one_click.ps1 -Path Sony-Web
  .\deploy_one_click.ps1 -Path Sony-Web -Merge  # (use with caution)
#>
param(
  [string]$Path = "Sony-Web",
  [string]$Branch = "",
  [string]$Message = "",
  [string]$Target = "main",
  [switch]$Merge
)

function Run-Git {
  param([string[]]$CmdArgs)
  $out = & git @CmdArgs 2>&1
  $ec = $LASTEXITCODE
  return @{ ExitCode = $ec; Out = $out }
}

# check git
$gt = Run-Git -CmdArgs @('--version')
if ($gt.ExitCode -ne 0) { Write-Error "Git no encontrado en PATH."; exit 1 }

$gitRootResult = Run-Git -CmdArgs @('rev-parse','--show-toplevel')
if ($gitRootResult.ExitCode -ne 0) { Write-Error "No se encontró un repositorio Git en el directorio actual."; exit 1 }
$gitRoot = $gitRootResult.Out -join ""; $gitRoot = $gitRoot.Trim()
Set-Location $gitRoot

if (-not (Test-Path $Path)) { Write-Error "Ruta '$Path' no encontrada dentro de $gitRoot"; exit 1 }

if (-not $Branch -or $Branch -eq "") {
  $timestamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
  $safePath = $Path -replace '[\\\/\s:]', '-'
  $Branch = "deploy-$safePath-$timestamp"
  Write-Host "Branch generado: $Branch"
}
if (-not $Message -or $Message -eq "") { $Message = "Auto: deploy $Path updates - $(Get-Date -Format 's')" }

# create or checkout branch
$check = Run-Git -CmdArgs @('rev-parse','--verify',$Branch)
if ($check.ExitCode -eq 0) {
  Write-Host "Usando branch existente: $Branch"
  & git checkout $Branch | Out-Null
} else {
  & git checkout -b $Branch | Out-Null
}

# stage path
& git add --all $Path

# check for staged changes
$status = & git status --porcelain
if (-not ($status -and $status.Trim())) {
  Write-Host "No hay cambios para commitear en '$Path'."
  exit 0
}

# commit
& git commit -m $Message
if ($LASTEXITCODE -ne 0) { Write-Error "Error en commit (¿conflictos o nada que commitear?): exit code $LASTEXITCODE"; exit 1 }

# push branch
& git push -u origin $Branch
if ($LASTEXITCODE -ne 0) { Write-Error "Push falló (revisa credenciales y conectividad)."; exit 1 }
Write-Host "Branch '$Branch' subido a origin."

# mostrar hint para PR
$remote = & git config --get remote.origin.url 2>$null
if ($LASTEXITCODE -eq 0 -and $remote) {
  $r = $remote.Trim()
  if ($r -match 'github.com[:/](.+?)(?:\.git)?$') {
    $repo = $matches[1]
    Write-Host "Crea un Pull Request: https://github.com/$repo/pull/new/$Branch"
  } else { Write-Host "Remote origin: $r" }
}

if ($Merge) {
  Write-Host "Intentando merge a $Target ...";
  & git checkout $Target
  & git pull origin $Target
  & git merge --no-ff $Branch -m "Merge $Branch -> $Target (auto)"
  if ($LASTEXITCODE -ne 0) { Write-Error "Merge falló. Resuelve localmente y vuelve a intentar."; exit 1 }
  & git push origin $Target
  Write-Host "Merge y push completados en $Target"
}

Write-Host "Hecho."