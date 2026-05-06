$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$failures = New-Object System.Collections.Generic.List[string]

function Add-Failure {
    param([string]$Message)
    $failures.Add($Message) | Out-Null
}

function Require-File {
    param([string]$RelativePath)
    $path = Join-Path $repoRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-Failure "Missing required file: $RelativePath"
    }
}

function Get-RelativePath {
    param([string]$Path)
    $root = (Resolve-Path -LiteralPath $repoRoot).Path.TrimEnd("\")
    $fullPath = (Resolve-Path -LiteralPath $Path).Path
    if ($fullPath.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $fullPath.Substring($root.Length + 1)
    }
    return $fullPath
}

$requiredFiles = @(
    "AGENTS.md",
    "docs/workflow-index.md",
    "docs/references/WORKFLOW_QUICKSTART.md",
    "docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md",
    "docs/references/SPEC_TEMPLATE.md",
    "docs/references/SPRINT_TEMPLATE.md",
    "docs/references/CHANGE_NOTE_TEMPLATE.md",
    "docs/references/SPEC_QA_TEMPLATE.md",
    "docs/references/SPRINT_QA_TEMPLATE.md"
)

foreach ($file in $requiredFiles) {
    Require-File $file
}

$requiredHeadings = @{
    "docs/references/WORKFLOW_QUICKSTART.md" = @("## Read Order", "## Choose The Path", "## QA Gate Rule", "## Evidence Rule", "## Validation Rule")
    "docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md" = @("## Core Agreement", "## QA Gate Semantics", "## Evidence Records", "## Workflow Index", "## Validation")
    "docs/references/SPEC_TEMPLATE.md" = @("## Evidence Log", "## Spec QA Record")
    "docs/references/SPRINT_TEMPLATE.md" = @("## Evidence Log", "## Sprint Doc QA", "## QA Report")
    "docs/references/CHANGE_NOTE_TEMPLATE.md" = @("## Evidence Log", "## QA Record")
    "docs/references/SPEC_QA_TEMPLATE.md" = @("- **Gate Decision:**", "### Evidence Reviewed")
    "docs/references/SPRINT_QA_TEMPLATE.md" = @("- **Gate Decision:**", "### Evidence Reviewed")
}

foreach ($entry in $requiredHeadings.GetEnumerator()) {
    $path = Join-Path $repoRoot $entry.Key
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        continue
    }
    $content = Get-Content -LiteralPath $path -Raw
    foreach ($heading in $entry.Value) {
        if ($content -notmatch [regex]::Escape($heading)) {
            Add-Failure "Missing heading '$heading' in $($entry.Key)"
        }
    }
}

$sprintRoot = Join-Path $repoRoot "docs/sprints"
if (Test-Path -LiteralPath $sprintRoot -PathType Container) {
    $sprintFiles = Get-ChildItem -LiteralPath $sprintRoot -Recurse -File -Filter "*.md"
    foreach ($file in $sprintFiles) {
        $relative = Get-RelativePath $file.FullName
        $content = Get-Content -LiteralPath $file.FullName -Raw
        $statusMatch = [regex]::Match($content, "(?m)^- \*\*Status:\*\* (.+)$")
        if (-not $statusMatch.Success) {
            Add-Failure "Missing Status metadata in $relative"
            continue
        }

        $status = $statusMatch.Groups[1].Value.Trim()
        $expectedFolder = switch ($status) {
            "Planned" { "docs\sprints\planned" }
            "Active" { "docs\sprints\active" }
            "Completed" { "docs\sprints\completed" }
            default { $null }
        }

        if ($null -eq $expectedFolder) {
            Add-Failure "Unknown sprint status '$status' in $relative"
        } elseif ($relative -notlike "$expectedFolder*") {
            Add-Failure "Sprint status/folder mismatch in $relative; status is $status"
        }

        if ($status -eq "Completed") {
            $blockedPatterns = @(
                "Pending implementation QA",
                "Not run yet",
                "None yet",
                "No completed sprints yet",
                "\[Command",
                "\[Summary",
                "\[None",
                "TBD"
            )
            foreach ($pattern in $blockedPatterns) {
                if ($content -match $pattern) {
                    Add-Failure "Completed sprint has unresolved placeholder '$pattern' in $relative"
                }
            }
        }
    }
}

if ($failures.Count -gt 0) {
    Write-Host "Workflow validation failed:" -ForegroundColor Red
    foreach ($failure in $failures) {
        Write-Host "- $failure" -ForegroundColor Red
    }
    exit 1
}

Write-Host "Workflow validation passed." -ForegroundColor Green
