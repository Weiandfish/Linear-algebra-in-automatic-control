$ErrorActionPreference = 'Stop'

$taskSources = @(Get-ChildItem -LiteralPath $PSScriptRoot -File -Filter 'Homework8_*.tex' | Sort-Object Name)
if ($taskSources.Count -lt 1) {
    throw 'No Homework8_*.tex source was found in this workspace.'
}
$taskEngine = (Get-Command 'xelatex.exe' -ErrorAction Stop).Source
$taskTempRoot = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$taskBuildName = 'codex-homework8-' + [Guid]::NewGuid().ToString('N')
$taskBuildPath = [System.IO.Path]::GetFullPath((Join-Path $taskTempRoot $taskBuildName))
$taskTempPrefix = $taskTempRoot.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar

# Validate the exact cleanup target before creating or deleting it.
if (-not $taskBuildPath.StartsWith($taskTempPrefix, [StringComparison]::OrdinalIgnoreCase) -or
    [System.IO.Path]::GetFileName($taskBuildPath) -notmatch '^codex-homework8-[0-9a-f]{32}$') {
    throw 'The build directory is outside the expected temporary directory.'
}
if ($taskBuildPath -match '[^\x00-\x7F]') {
    throw 'This XeLaTeX installation requires an ASCII temporary build path.'
}

$taskLocationPushed = $false
try {
    New-Item -ItemType Directory -Path $taskBuildPath | Out-Null
    $taskSourceIndex = 0
    foreach ($taskSource in $taskSources) {
        $taskSourceIndex++
        $taskDocumentBuild = Join-Path $taskBuildPath ("document-$taskSourceIndex")
        New-Item -ItemType Directory -Path $taskDocumentBuild | Out-Null
        Copy-Item -LiteralPath $taskSource.FullName -Destination (Join-Path $taskDocumentBuild 'homework8.tex')
        Push-Location -LiteralPath $taskDocumentBuild
        $taskLocationPushed = $true

        for ($taskPass = 1; $taskPass -le 3; $taskPass++) {
            & $taskEngine -interaction=nonstopmode -halt-on-error -file-line-error 'homework8.tex' > 'compiler-output.txt' 2>&1
            if ($LASTEXITCODE -ne 0) {
                Get-Content -LiteralPath 'compiler-output.txt' -Tail 35
                throw "XeLaTeX failed on pass $taskPass for $($taskSource.Name)."
            }
            $taskLog = Get-Content -LiteralPath 'homework8.log' -Raw
        }
        $taskOutputPdf = [System.IO.Path]::ChangeExtension($taskSource.FullName, '.pdf')
        Copy-Item -LiteralPath 'homework8.pdf' -Destination $taskOutputPdf -Force
        Write-Output "Compiled successfully: $taskOutputPdf"
        if ($taskLog -match 'Overfull|Missing character|LaTeX Warning|Package .* Warning') {
            Write-Output 'Compiler notices:'
            Select-String -LiteralPath 'homework8.log' -Pattern 'Overfull|Missing character|LaTeX Warning|Package .* Warning' |
                ForEach-Object { Write-Output $_.Line }
        }
        Pop-Location
        $taskLocationPushed = $false
    }
}
finally {
    if ($taskLocationPushed) { Pop-Location }
    # Recheck the normalized absolute path immediately before recursive cleanup.
    $taskCleanupPath = [System.IO.Path]::GetFullPath($taskBuildPath)
    if (-not $taskCleanupPath.StartsWith($taskTempPrefix, [StringComparison]::OrdinalIgnoreCase) -or
        [System.IO.Path]::GetFileName($taskCleanupPath) -notmatch '^codex-homework8-[0-9a-f]{32}$') {
        throw 'Refusing to clean an unexpected build directory.'
    }
    if (Test-Path -LiteralPath $taskCleanupPath -PathType Container) {
        Remove-Item -LiteralPath $taskCleanupPath -Recurse -Force
    }
}
