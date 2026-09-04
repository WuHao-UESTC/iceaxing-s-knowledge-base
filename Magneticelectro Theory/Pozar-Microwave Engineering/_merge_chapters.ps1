$ErrorActionPreference = "Stop"
$base = "E:\base_Obsidian\iceaxing's knowledge base\Magneticelectro Theory\Pozar-Microwave Engineering"

# Define chapter groups: ordered list of (prefix, chapter_title, output_filename)
$chapters = @(
    @{Prefix="02-"; Title="传输线理论";         Output="02-传输线理论.md"},
    @{Prefix="03-"; Title="传输线与波导";       Output="03-传输线与波导.md"},
    @{Prefix="04-"; Title="微波网络分析";       Output="04-微波网络分析.md"},
    @{Prefix="05-"; Title="阻抗匹配与调谐";     Output="05-阻抗匹配与调谐.md"},
    @{Prefix="07-"; Title="功分器与耦合器";     Output="07-功分器与耦合器.md"},
    @{Prefix="08-"; Title="微波滤波器";         Output="08-微波滤波器.md"},
    @{Prefix="09-"; Title="铁氧体器件";         Output="09-铁氧体器件.md"},
    @{Prefix="10-"; Title="噪声与非线性失真";   Output="10-噪声与非线性失真.md"},
    @{Prefix="11-"; Title="有源射频微波器件";   Output="11-有源射频微波器件.md"},
    @{Prefix="12-"; Title="微波放大器设计";     Output="12-微波放大器设计.md"},
    @{Prefix="13-"; Title="振荡器与混频器";     Output="13-振荡器与混频器.md"},
    @{Prefix="14-"; Title="微波系统导论";       Output="14-微波系统导论.md"}
)

foreach ($ch in $chapters) {
    $prefix = $ch.Prefix
    $title = $ch.Title
    $outputFile = Join-Path $base $ch.Output

    # Find matching files, sorted
    $files = Get-ChildItem -Path $base -Filter "$prefix*.md" | Sort-Object Name
    if ($files.Count -eq 0) {
        Write-Host "SKIP: no files found for prefix '$prefix'"
        continue
    }
    Write-Host "=== Merging $($files.Count) files -> $($ch.Output) ==="

    $mergedContent = @()
    $mergedContent += "# $title"
    $mergedContent += ""

    foreach ($f in $files) {
        Write-Host "  + $($f.Name)"
        $raw = Get-Content -Path $f.FullName -Raw -Encoding UTF8

        # Demote headings: must go deepest-first to avoid double-demotion
        # Replace #### → #####, ### → ####, ## → ###, # → ##
        # Use a marker approach to avoid cascade
        $raw = $raw -replace '#### ', '##### '
        $raw = $raw -replace '### ', '#### '
        $raw = $raw -replace '## ', '### '
        $raw = $raw -replace '# ', '## '

        # Trim trailing whitespace but preserve internal structure
        $raw = $raw.TrimEnd()

        $mergedContent += $raw
        $mergedContent += ""
        $mergedContent += "---"
        $mergedContent += ""
    }

    # Write merged file
    $final = ($mergedContent -join "`r`n").TrimEnd() + "`r`n"
    [System.IO.File]::WriteAllText($outputFile, $final, [System.Text.UTF8Encoding]::new($true))
    Write-Host "  -> Written: $($ch.Output) ($([math]::Round($final.Length/1024, 1)) KB)"

    # Delete original files
    foreach ($f in $files) {
        Remove-Item -Path $f.FullName -Force
        Write-Host "  x Deleted: $($f.Name)"
    }
}

Write-Host ""
Write-Host "=== Done! ==="
